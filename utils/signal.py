from psutil import Process, wait_procs
from signal import SIGTERM

__all__ = [
    'send_tree'
]


def send_tree(pid, sig=SIGTERM, include_parent=True, timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal "sig" and return a (gone, still_alive) tuple.
       "on_terminate", if specified, is a callback function which is called as soon as a child terminates."""
    parent = Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        p.send_signal(sig)
    gone, alive = wait_procs(children, timeout=timeout, callback=on_terminate)
    return (gone, alive)
