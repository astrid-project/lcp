from docstring import docstring
from lib.http import HTTP_Method
from lib.parser import *
from lib.response import *
from resource.base import Base_Resource
from schema.config import *
from schema.response import *
from utils.datetime import datetime_to_str
from utils.json import loads
from utils.sequence import is_list, table_to_dict, wrap
from utils.signal import send_tree
from os.path import expanduser as expand_user
from utils.exception import extract_info

import signal
import subprocess as sp
import time

File_Not_Found_Error = FileNotFoundError

__all__ = [
    'Config_Resource'
]


class Config_Resource(Base_Resource):
    tag = dict(name='config', description='Configuration at run-time.')
    routes = '/config',
    parsers = dict(json=json_parser,
                   properties=property_parser,
                   xml=xml_parser,
                   yaml=yaml_parser)

    @docstring(source='config/post.yaml')
    def on_post(self, req, resp):
        req_data = req.media or {}
        resp_data, valid = Config_Request_Schema(many=is_list(req_data),
                                                 method=HTTP_Method.POST).validate(data=req_data)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for config in req_data_wrap:
                    for cfg, cfg_list in config.items():
                        for data in wrap(cfg_list):
                            if cfg == 'actions':
                                output = self.__actions(data)
                                schema = Config_Action_Response_Schema
                            elif cfg == 'parameters':
                                output = self.__parameters(data)
                                schema = Config_Parameter_Response_Schema
                            elif cfg == 'resources':
                                output = self.__resources(data)
                                schema = Config_Resource_Response_Schema
                            output.update(id=data.get('id', None),
                                          timestamp=datetime_to_str())
                            resp_data, valid = schema(
                                many=False, method=HTTP_Method.POST).validate(data=output)
                            if valid:
                                Content_Response(output).add(resp)
                            else:
                                resp_data.add(resp)
            else:
                msg = f'No content to apply configurations with the {{request}}'
                No_Content_Response(msg, request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    def __actions(self, data):
        cmd = data.get('cmd', None)
        daemon = data.get('daemon', False)
        output = dict(type='action')
        run = ' '.join([cmd] + wrap(data.get('args', [])))
        start = time.time()
        proc = self.__run_cmd(cmd=run, daemon=daemon, output=output)
        if daemon:
            output.update(error=False, executed=run, return_code=0)
        else:
            output.update(error=proc.returncode != 0, executed=run,
                          return_code=proc.returncode, duration=time.time() - start)
            self.__set_std(proc.stdout, output, 'stdout')
            self.__set_std(proc.stderr, output, 'stderr')
        return output

    def __parameters(self, data):
        schema = data.get('schema', None)
        source = data.get('source', None)
        path = wrap(data.get('path', None))
        value = data.get('value', None)
        output = dict(type='parameter')
        try:
            source = expand_user(source)
            output.update(self.parsers.get(schema)
                          (schema, source, path, value))
        except File_Not_Found_Error as e:
            msg = f'Source {source} not found'
            self.log.exception(msg, e)
            output.update(error=True, data=data,
                          description=msg, exception=extract_info(e))
        except Exception as e:
            msg = f'Source {source} not accessible'
            self.log.exception(msg, e)
            output.update(error=True, data=data,
                          description=msg, exception=extract_info(e))
        return output

    def __resources(self, data):
        path = data.get('path', None)
        content = data.get('content', None)
        output = dict(type='resource')
        try:
            fix_path = expand_user(path)
            with open(fix_path, "w") as file:
                file.write(content)
                output.update(path=path, content=content)
        except FileNotFoundError as e:
            msg = f'Path {path} not found'
            self.log.exception(msg, e)
            output.update(error=True, data=data,
                          description=msg, exception=extract_info(e))
        except Exception as e:
            msg = f'Path {path} not accessible'
            self.log.exception(msg, e)
            output.update(error=True, data=data,
                          description=msg, exception=extract_info(e))
        return output

    def __set_std(self, data, output, key):
        if data:
            output[key] = data.splitlines()

    def __run_cmd(self, cmd, daemon, output):
        if not daemon:
            return sp.run(cmd, check=False, shell=True,
                          stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
        else:
            output.update(daemon=daemon)
            return sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, start_new_session=True)
