import coloredlogs
import logging

from args import Args
from verboselogs import VerboseLogger


class Log(VerboseLogger):
    """
    Wrapper class for coloured and verbuse logs.
    """

    @staticmethod
    def get(name):
        """
        Return the initialized logger with the module name.

        :param name: module name
        :returns: logger instance
        """
        coloredlogs.install(level=Args.db.log_level)
        logger = VerboseLogger(name)
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def get_levels():
        """
        Get list of log level names.

        :returns: list of string
        """
        return logging._levelToName.values()
