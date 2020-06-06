from utils.json import loads
from utils.sequence import exclude_keys
from utils.signal import send_tree

import subprocess as sp


def make_actions(self, data):
    type = 'action'
    cmd = data.get('cmd', None)
    if cmd is None:
        output = dict(error=True, type=type, data=data,
                      description='Missing cmd')
    else:
        daemon = data.get('daemon', None)
        if cmd.startswith('@') and cmd in ('@stop', '@restart'):
            if daemon is None:
                output = dict(error=True, type=type, data=data,
                              description='Missing daemon')
            else:
                if cmd == '@stop':
                    daemon_pid = self.daemon_pids.pop(daemon, None)
                    sig = signal.SIGTERM
                else:
                    daemon_pid = self.daemon_pids.get(daemon, None)
                    sig = signal.SIGHUP  # FIXME in Windows not work!
                if daemon_pid is None:
                    output = dict(error=True, type=type, data=data,
                                  description=f'Daemon {daemon} not found')
                else:
                    try:
                        send_tree(daemon_pid, sig=sig)
                        output = dict(type=type, cmd=cmd,
                                      daemon=daemon, pid=daemon_pid)
                    except Exception as exception:
                        self.log.error(f'Exception: {exception}')
                        output = dict(error=True, type=type, data=data, exception=str(exception),
                                      description=f'{cmd.replace("@", "").title()} {daemon} not possible')
        else:
            run = ' '.join([cmd] + data.get('args', []))
            if not daemon:
                proc = sp.run(run, check=False, shell=True,
                              stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
            else:
                proc = sp.Popen(run, shell=True, stdout=sp.PIPE, stderr=sp.PIPE,
                                creationflags=sp.DETACHED_PROCESS, start_new_session=True)
                self.daemon_pids[daemon] = proc.pid
            output = dict(type=type, error=proc.returncode != 0, executed=run,
                          **{'return-code': proc.returncode})
            if proc.stdout:
                try:
                    output['stdout'] = loads(proc.stdout)
                except Exception as exception:
                    output['stdout'] = proc.stdout.splitlines()
            if proc.stderr:
                try:
                    output['stderr'] = loads(proc.stderr)
                except Exception as exception:
                    output['stderr'] = proc.stderr.splitlines()
            if daemon:
                output['daemon'] = daemon
    useless_properties = exclude_keys(data, 'cmd', 'args', 'daemon')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
