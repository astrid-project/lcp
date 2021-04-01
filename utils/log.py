import logging
import os
import sys
from functools import partial, partialmethod
from inspect import stack

import yaml
from bunch import Bunch
from emoji import emojize
from loguru import logger
from rich.console import Console
from yaml import FullLoader as Full_Loader

from about import name as about_name

emoji = partial(emojize, use_aliases=True)
console = Console()


class Formatter:
    @staticmethod
    def info(name):
        for s in stack():
            if name in s.filename.replace('_', '-'):
                return s
        return None

    @classmethod
    def apply(cls, record):
        # s = cls.info(record['name'])
        # record['called'] = Bunch(filename=path.basename(s.filename), function=s.function, lineno=s.lineno, icon=emoji(':computer:'))
        record['called'] = Bunch(filename=record['file'].name, function=record['function'], lineno=record['line'], icon=emoji(':computer:'))
        record['elapsed'] = Bunch(time=record['elapsed'], icon=emoji(':alarm_clock:'))
        record['message'] = emoji(record['message'])


class Log:
    default_icon = ':small_orange_diamond:'

    @classmethod
    def init(cls, config):
        """Set the default and levels and initialize the log manager.

        :param cls: Log class.
        :param config: Path of the config filename
        :param clear: Clear the previous logs.
        """
        with open(config) as cfg_file:
            cfg = yaml.load(cfg_file, Loader=Full_Loader)
        levels = cfg.get('levels', [])
        for level in levels:
            level['icon'] = emoji(level.get('icon', cls.default_icon))
            name = level.get('name', None)
            if name:
                klass = type(logger)
                setattr(klass, name.lower(), partialmethod(klass.log, name))
        hdls = []
        for sink_data in cfg.get('sinks', []):
            if sink_data.get('enabled', True):
                klass = sink_data.get('klass', None)
                if klass:
                    if klass.lower() == 'stdout':
                        sink = sys.stdout
                    elif klass.lower() == 'stderr':
                        sink = sys.stderr
                    else:
                        sink = klass.format(name=name)
                        if sink_data.get('clear', True) and os.path.exists(sink):
                            os.remove(sink)
                    h = dict(sink=sink, **sink_data.get('args', {}))
                    hdls.append(h)
        logger.configure(handlers=hdls, levels=cfg.get('levels', {}), patcher=Formatter.apply)

        for level in levels:
            cls.get('log').info(f"Found additional log level customization: {level['icon']:<3} {level['name']}")

    @classmethod
    def get(cls, name=about_name):
        return logger.bind(context=name).opt(colors=True)

    @staticmethod
    def get_levels():
        """Get list of log level names.

        :returns: list of string
        """
        return list(logging._levelToName.values())
