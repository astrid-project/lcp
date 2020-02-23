# cspell:ignore strftime

from .base import BaseResource
from datetime import datetime
from utils import exclude_keys_from_dict, get_none, wrap
from schema import ConfigRequestSchema, ConfigResponseSchema
import falcon
import re
import subprocess


class ConfigResource(BaseResource):
    request_schema = ConfigRequestSchema()
    response_schema = ConfigResponseSchema()

    routes = '/config',
    history_filename = 'data/config.history'

    def on_get(self, req, resp):
        """
        Get the history of configuration updates.
        ---
        summary: Configuration update history
        description: Get the history of configuration updates.
        tags: [config]
        responses:
            200:
                description: History of the configuration updates.
                schema:
                    type: array
                    items: ConfigResponseSchema
            400:
                description: Bad Request.
                schema: BadRequestSchema
            401:
                description: Unauthorized.
                schema: UnauthorizedSchema
        """
        req.context['result'] = self.history

    def on_post(self, req, resp):
        """
        Apply configuration changes to the local environment.
        ---
        summary: Configuration update
        description: Apply configuration changes to the local environment.
        tags: [config]
        parameters:
            - name: payload
              required: true
              in: body
              schema: ConfigRequestSchema
        responses:
            200:
                description: Configuration changes executed.
                schema: ConfigResponseSchema
            400:
                description: Bad request.
                schema: BadRequestSchema
            401:
                description: Unauthorized.
                schema: UnauthorizedSchema
        """
        json = req.context.get('json', None)
        if json is not None:
            res = {
                'when': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                'results': []
            }
            for config in wrap(json):
                for cfg, cfg_list in config.items():
                        for data in wrap(cfg_list):
                            if cfg == 'actions':
                                type = 'action'
                                cmd = data.get('cmd', None)
                                if cmd is None:
                                    output = dict(type=type, error=True, description='Missing cmd')
                                else:
                                    run = cmd + ' ' + ' '.join(data.get('args', ''))
                                    try:
                                        process = subprocess.run('bash -c "' + run + '"', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                                    except Exception as e:
                                        output = dict(type=type, error=True, description=str(e))
                                    else:
                                        output = dict(type=type, executed=run, stdout=process.stdout, stderr=process.stderr, **{'return-code': process.returncode})
                                useless_properties = exclude_keys_from_dict(data, 'cmd', 'args')
                                if len(useless_properties) > 0:
                                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                            elif cfg == 'parameters':
                                type = 'parameter'
                                dest = data.get('destination', None)
                                name = data.get('name', None)
                                sep = data.get('sep', None)
                                value = data.get('value', None)
                                if dest is None or name is None or sep is None or value is None:
                                    output = dict(type=type, error=True, description=f'Missing {get_none(destination=dest, name=name, sep=sep, value=value)}')
                                else:
                                    try:
                                        with open(dest, "r") as file:
                                            content = file.read()
                                        with open(dest, "w") as file:
                                            file.write(re.sub(rf"{name}{sep}[^ ]*", f"{name}{sep}{value}", content))
                                            output = dict(type=type, destination=dest, name=name, value=value)
                                    except FileNotFoundError:
                                        output = dict(type=type, error=True, description=f'Destination {dest} not found')
                                    except:
                                        output = dict(type=type, error=True, description=f'Destination {dest} not accessible')
                                useless_properties = exclude_keys_from_dict(data, 'destination', 'name', 'sep', 'value')
                                if len(useless_properties) > 0:
                                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                            elif cfg == 'resources':
                                type = 'resource'
                                dest = data.get('destination', None)
                                content = data.get('content', None)
                                if dest is None or content is None:
                                    output = dict(type=type, error=True, description=f'Missing {get_none(destination=dest, content=content)}')
                                else:
                                    try:
                                        with open(dest, "w") as file:
                                            file.write(content)
                                            output = dict(type=type, destination=dest)
                                    except FileNotFoundError:
                                        output = dict(type=type, error=True, description=f'Destination {dest} not found')
                                    except:
                                        output = dict(type=type, error=True, description=f'Destination {dest} not accessible')
                                useless_properties = exclude_keys_from_dict(data, 'destination', 'content')
                                if len(useless_properties) > 0:
                                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                            else:
                                output = dict(type=cfg, error=True, description='Request type unknown')
                            res['results'].append(output)
            req.context['result'] = res
            self.history.append(res)
        else:
            raise falcon.HTTPBadRequest(title='Request error', description='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
