from docstring import docstring
from falcon.errors import HTTPBadRequest
from lib.parser import json_parser, property_parser, yaml_parser
from resource.base import BaseResource
from schema.config import ConfigRequestSchema, ConfigResponseSchema
from schema.http_error import HTTPErrorSchema
from schema.validate import validate
from utils.datetime import datetime_to_str
from utils.json import loads
from utils.sequence import wrap
from utils.signal import send_tree
from os.path import expanduser
from utils.data import get_none


import signal
import subprocess as sp


class ConfigResource(BaseResource):
    daemon_pids = {}
    tag = dict(name='config', description='Configuration at run-time.')
    routes = '/config',
    parsers = dict(json=json_parser,
                   properties=property_parser, yaml=yaml_parser)

    @docstring(source='config/post.yaml')
    def on_post(self, req, resp):
        req_data = validate(schema=ConfigRequestSchema(),
                            method='POST', data=req.media)
        resp_data = dict(when=datetime_to_str(), results=[])
        for config in wrap(req_data):
            for cfg, cfg_list in config.items():
                for data in wrap(cfg_list):
                    if cfg == 'actions':
                        output = self.__actions(data)
                    elif cfg == 'parameters':
                        output = self.__parameters(data)
                    elif cfg == 'resources':
                        output = self__resources(data)
                    resp_data['results'].append(output)
        # TODO
        # resp.media = validate(schema=ConfigResponseSchema(
        #     unknown='INCLUDE'), method='POST', data=resp_data)
        resp.media = resp_data

    def __actions(self, data):
        cmd = data.get('cmd', None)
        daemon = data.get('daemon', None)
        output = dict(type='action')
        # TODO validate daemon if cmd @stop, @restart
        if cmd.startswith('@') and cmd in ('@stop', '@restart'):
            output = self.__run_daemon(cmd=cmd, daemon=daemon)
        else:
            run = ' '.join([cmd] + data.get('args', []))
            proc = self.__run_cmd(cmd=run, daemon=daemon, output=output)
            output.update(error=proc.returncode != 0, executed=run,
                          return_code=proc.returncode)
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
            source = expanduser(source)
            output.update(self.parsers.get(schema)
                          (schema, source, path, value))
        except FileNotFoundError as file_not_found_error:
            self.log.error(f'Exception: {file_not_found_error}')
            output.update(error=True, type=type, data=data, description=f'Source {source} not found',
                          exception=str(file_not_found_error))
        except Exception as exception:
            self.log.error(f'Exception: {exception}')
            output.update(error=True, type=type, data=data, description=f'Source {source} not accessible',
                          exception=str(exception))
        return output

    def __resources(self, data):
        type = 'resource'
        path = data.get('path', None)
        content = data.get('content', None)
        try:
            fix_path = expanduser(path)
            with open(fix_dest, "w") as file:
                file.write(content)
                output = dict(type=type, path=path)
        except FileNotFoundError as file_not_found_error:
            self.log.error(f'Exception: {file_not_found_error}')
            output = dict(type=type, error=True,
                          description=f'Path [path] not found', data=data)
        except Exception as exception:
            self.log.error(f'Exception {exception}')
            output = dict(type=type, error=True,
                          description=f'Path [path] not accessible', data=data)
        return output

    def __set_std(self, data, output, key):
        if data:
            try:
                data = data.replace('Size of the terminal is too small, output could be missaligned.', '') \
                           .replace(' id ', ' n ')
                output[key] = loads(data)
            except Exception as exception:
                output[key] = data.splitlines()

    def __run_cmd(self, cmd, daemon, output):
        if not daemon:
            return sp.run(cmd, check=False, shell=True,
                          stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
        else:
            # FIXME DETACHED_PROCESS is linux not work
            output.update(daemon=daemon)
            return sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE,
                            creationflags=sp.DETACHED_PROCESS, start_new_session=True)

    def __run_daemon(self, cmd, daemon):
        if cmd == '@stop':
            daemon_pid = self.daemon_pids.pop(daemon, None)
            sig = signal.SIGTERM
        else:
            daemon_pid = self.daemon_pids.get(daemon, None)
            sig = signal.SIGHUP  # FIXME in Windows not work!
        if daemon_pid is None:
            return dict(error=True, type=type, data=data,
                        description=f'Daemon {daemon} not found')
        else:
            try:
                send_tree(daemon_pid, sig=sig)
                return dict(type=type, cmd=cmd,
                            daemon=daemon, pid=daemon_pid)
            except Exception as exception:
                self.log.error(f'exception: {exception}')
                return dict(error=True, type=type, data=data, exception=str(exception),
                            description=f'{cmd.replace("@", "").title()} {daemon} not possible')
