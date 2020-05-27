def make_actions(self, data):
    type = 'action'
    cmd = data.get('cmd', None)
    if cmd is None:
        output = dict(type=type, error=True, description='Missing cmd')
    else:
        daemon = data.get('daemon', None)
        if cmd.startswith('@'):
            if cmd in ('@stop', '@restart'):
                if daemon is None:
                    output = dict(type=type, error=True, description='Missing daemon')
                else:
                    if cmd == '@stop':
                        daemon_pid = self.daemon_pids.pop(daemon, None)
                        sig = signal.SIGTERM
                    else:
                        daemon_pid = self.daemon_pids.get(daemon, None)
                        sig = signal.SIGHUP # FIXME in Windows not work!

                    if daemon_pid is None:
                        output = dict(type=type, error=True, description=f'Daemon {daemon} not found')
                    else:
                        try:
                            send_signal_tree(daemon_pid, sig=sig)
                            output = dict(type=type, cmd=cmd, daemon=daemon, pid=daemon_pid)
                        except Exception as e:
                            self.log.debug(e)
                            cmd_name = cmd.replace("@", "").title()
                            output = dict(type=type, error=True, description=f'{cmd_name} {daemon} not possible', exception=str(e))
            else:
                output = dict(type=type, error=True, description=f'Action {cmd} unknown')
        else:
            run = cmd + ' ' + ' '.join(data.get('args', ''))
            try:
                if not daemon:
                    proc = sp.run(run, check=True, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
                    output = dict(type=type, executed=run, stdout=proc.stdout,
                                    stderr=proc.stderr, **{'return-code': proc.returncode})
                else:
                    proc = sp.Popen(run, stdout=sp.PIPE, stderr=sp.PIPE, shell=True,
                                    creationflags=sp.DETACHED_PROCESS, start_new_session=True)
                    self.daemon_pids[daemon] = proc.pid
                    output = dict(type=type, executed=run, daemon=daemon)
            except Exception as e:
                self.log.debug(e)
                output = dict(type=type, error=True, description=str(e))
    useless_properties = exclude_keys(data, 'cmd', 'args', 'daemon')
    if len(useless_properties) > 0:
        output['warning'] = f'Useless properties: {", ".join(useless_properties.keys())}'
    return output
