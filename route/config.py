# cspell:ignore strftime

from .base import BaseResource
from datetime import datetime
from utils import exclude_keys_from_dict, get_none, wrap
from schema import ConfigRequest, ConfigResponse
import falcon
import re
import subprocess


class ConfigResource(BaseResource):
    request_schema = ConfigRequest()
    response_schema = ConfigResponse()

    route = ['/config']

    def on_post(self, req, resp):
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
                                    run = cmd + ' '.join(data.get('args', ''))
                                    process = subprocess.run(run, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
        else:
            raise falcon.HTTPBadRequest(title="Request error", description="Empty request")
