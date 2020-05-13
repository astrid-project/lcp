from .base import BaseResource
from schema import *

import os
import falcon
import re
import subprocess
import utils


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
                    items:
                        oneOf:
                            - ConfigActionResponseSchema
                            - ConfigParameterResponseSchema
                            - ConfigResourceResponseSchema
            400:
                description: Bad Request.
                schema: HTTPErrorSchema
            401:
                description: Unauthorized.
                schema: HTTPErrorSchema
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
              schema:
                type: array
                items: ConfigRequestSchema
        responses:
            200:
                description: Configuration changes executed.
                schema:
                    type: array
                    items: ConfigResponseSchema
            400:
                description: Bad request.
                schema: HTTPErrorSchema
            401:
                description: Unauthorized.
                schema: HTTPErrorSchema
        """
        json = req.context.get('json', None)
        if json is not None:
            res = {
                'when': utils.datetime_to_str(),
                'results': []
            }
            for config in utils.wrap(json):
                for cfg, cfg_list in config.items():
                        for data in utils.wrap(cfg_list):
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
                                        log.debug(e)
                                        output = dict(type=type, error=True, description=str(e))
                                    else:
                                        output = dict(type=type, executed=run, stdout=process.stdout, stderr=process.stderr, **{'return-code': process.returncode})
                                useless_properties = utils.exclude_keys_from_dict(data, 'cmd', 'args')
                                if len(useless_properties) > 0:
                                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                            elif cfg == 'parameters':
                                type = 'parameter'
                                dest = data.get('destination', None)
                                name = data.get('name', None)
                                sep = data.get('sep', None)
                                value = data.get('value', None)
                                if dest is None or name is None or sep is None or value is None:
                                    output = dict(type=type, error=True, description=f'Missing {utils.get_none(destination=dest, name=name, sep=sep, value=value)}')
                                else:
                                    try:
                                        fix_dest = os.path.expanduser(dest)
                                        with open(fix_dest, "r") as file:
                                            content = file.read()
                                        with open(fix_dest, "w") as file:
                                            file.write(re.sub(rf"{name}{sep}[ ]*[^ ]*\n", f"{name}{sep} {value}\n", content))
                                            output = dict(type=type, destination=dest, name=name, value=value)
                                    except FileNotFoundError as fnfe:
                                        self.log.debug(fnfe)
                                        output = dict(type=type, error=True, description=f'Destination {dest} not found')
                                    except Exception as e:
                                        self.log.debug(e)
                                        output = dict(type=type, error=True, description=f'Destination {dest} not accessible')
                                useless_properties = utils.exclude_keys_from_dict(data, 'destination', 'name', 'sep', 'value')
                                if len(useless_properties) > 0:
                                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                            elif cfg == 'resources':
                                type = 'resource'
                                dest = data.get('destination', None)
                                content = data.get('content', None)
                                if dest is None or content is None:
                                    output = dict(type=type, error=True, description=f'Missing {utils.get_none(destination=dest, content=content)}')
                                else:
                                    try:
                                        fix_dest = os.path.expanduser(dest)
                                        with open(fix_dest, "w") as file:
                                            file.write(content)
                                            output = dict(type=type, destination=dest)
                                    except FileNotFoundError as fnfe:
                                        self.log.debug(fnfe)
                                        output = dict(type=type, error=True, description=f'Destination {dest} not found')
                                    except Exception as e:
                                        self.log.debug(e)
                                        output = dict(type=type, error=True, description=f'Destination {dest} not accessible')
                                useless_properties = utils.exclude_keys_from_dict(data, 'destination', 'content')
                                if len(useless_properties) > 0:
                                    output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
                            else:
                                output = dict(type=cfg, error=True, description='Request type unknown')
                            res['results'].append(output)
            req.context['result'] = res
            self.history.append(res)
        else:
            raise falcon.HTTPBadRequest(title='Request error', description='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
