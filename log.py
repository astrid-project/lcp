import coloredlogs
import logging

from args import Args
from verboselogs import VerboseLogger


class Log(VerboseLogger):
    """
    Wrapper class for coloured and verbuse logs.
    """
    levels = {}

    @classmethod
    def get(cls, name):
        """
        Return the initialized logger with the module name.

        :param cls: Log class.
        :param name: module name
        :returns: logger instance
        """
        level = cls.levels.get(name, Args.db.log_level)
        coloredlogs.install(level=level)
        logger = VerboseLogger(name)
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(level)
        return logger

    @staticmethod
    def get_levels():
        """
        Get list of log level names.

        :returns: list of string
        """
        return logging._levelToName.values()

    @classmethod
    def set_levels(cls, levels):
        """
        Set the log level for each module.

        :params cls: Log class.
        :params levels: list of tuple (module, level)
        """
        cls.levels = { module: level for module, level in levels}
        for module, level in levels:
            logger = logging.getLogger(module)
            logger.setLevel(level)
