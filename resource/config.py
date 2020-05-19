from .base import BaseResource
from jproperties import Properties
from schema import *

import falcon
import json as json_lib
import os
import re
import subprocess as sp
import utils
import yaml


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

    def make_actions(self, data):
        type = 'action'
        cmd = data.get('cmd', None)
        if cmd is None:
            output = dict(type=type, error=True, description='Missing cmd')
        else:
            run = cmd + ' ' + ' '.join(data.get('args', ''))
            try:
                proc = sp.run('bash -c "' + run + '"', check=True,
                              stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
            except Exception as e:
                log.debug(e)
                output = dict(type=type, error=True, description=str(e))
            else:
                output = dict(type=type, executed=run, stdout=proc.stdout,
                              stderr=proc.stderr, **{'return-code': proc.returncode})
        useless_properties = utils.exclude_keys_from_dict(data, 'cmd', 'args')
        if len(useless_properties) > 0:
            output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
        return output

    def make_parameters(self, data):
        type = 'parameter'
        schema = data.get('schema', None)
        source = data.get('source', None)
        path = data.get('path', None)
        value = data.get('value', None)
        if schema is None or source is None or path is None or value is None:
            output = dict(type=type, error=True,
                          description=f'Missing {utils.get_none(schema=schema, source=source, path=path, value=value)}')
        elif schema not in ['yaml', 'json', 'properties']:
            output = dict(type=type, error=True,
                          description=f'Schema {schema} not valid. Must be one of yaml, json or properties')
        else:
            path = utils.wrap(path)
            try:
                source = os.path.expanduser(source)
                if schema == 'yaml':
                    with open(source, "r") as file:
                        content = yaml.load(file, Loader=yaml.FullLoader)
                        d = utils.iter_dict(content, *path[:-1])
                        old_value = d[path[-1]]
                        if old_value != value:
                            d[path[-1]] = value
                            with open(source, 'w') as file:
                                yaml.dump(content, file,
                                          sort_keys=True, indent=3)
                                output = dict(type=type, schema=schema, source=source, path=path, value={
                                                 'new': value, 'old': old_value})
                        else:
                            output = dict(type=type, schema=schema, source=source,
                                          path=path, value=value, note='No change needed')
                elif schema == 'json':
                    with open(source, 'r') as file:
                        content = json_lib.load(file)
                        d = utils.iter_dict(content, *path[:-1])
                        old_value = d[path[-1]]
                        if old_value != value:
                            d[path[-1]] = value
                            with open(source, 'w') as file:
                                json_lib.dump(
                                    content, file, sort_keys=True, indent=3)
                                output = dict(type=type, schema=schema, source=source, path=path, value={
                                                'new': value, 'old': old_value})

                        else:
                            output = dict(type=type, schema=schema, source=source,
                                          path=path, value=value, note='No change needed')
                elif schema == 'properties':
                    with open(source, 'rb') as file:
                        content = Properties()
                        content.load(file, 'utf-8')
                        k = '.'.join(path)
                        old_value, _ = content[k]
                        if old_value != value:
                            content[k] = value
                            with open(source, 'wb') as file:
                                content.store(file, encoding='utf-8')
                                output = dict(type=type, schema=schema, source=source, path=path, value={
                                                'new': value, 'old': old_value})
                        else:
                            output = dict(type=type, schema=schema, source=source,
                                          path=path, value=value, note='No change needed')
            except FileNotFoundError as file_not_found_error:
                self.log.debug(file_not_found_error)
                output = dict(
                    type=type, error=True, description=f'Source {source} not found')
            except Exception as e:
                self.log.debug(e)
                output = dict(type=type, error=True,
                              description=f'Source {source} not accessible')
        useless_properties = utils.exclude_keys_from_dict(
            data, 'schema', 'source', 'path', 'value')
        if len(useless_properties) > 0:
            output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
        return output

    def make_resources(data):
        type = 'resource'
        dest = data.get('destination', None)
        content = data.get('content', None)
        if dest is None or content is None:
            output = dict(type=type, error=True,
                          description=f'Missing {utils.get_none(destination=dest, content=content)}')
        else:
            try:
                fix_dest = os.path.expanduser(dest)
                with open(fix_dest, "w") as file:
                    file.write(content)
                    output = dict(type=type, destination=dest)
            except FileNotFoundError as file_not_found_error:
                self.log.debug(file_not_found_error)
                output = dict(
                    type=type, error=True, description=f'Destination {dest} not found')
            except Exception as e:
                self.log.debug(e)
                output = dict(type=type, error=True,
                              description=f'Destination {dest} not accessible')
        useless_properties = utils.exclude_keys_from_dict(
            data, 'destination', 'content')
        if len(useless_properties) > 0:
            output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
        return output

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
                            output = self.make_actions(data)
                        elif cfg == 'parameters':
                            output = self.make_parameters(data)
                        elif cfg == 'resources':
                            output = self.make_resources(data)
                        else:
                            output = dict(type=cfg, error=True,
                                          description='Request type unknown')
                        res['results'].append(output)
            req.context['result'] = res
            self.history.append(res)
        else:
            raise falcon.HTTPBadRequest(
                title='Request error', description='Could not decode the request body, either because it was not valid JSON or because it was not encoded as UTF-8.')
