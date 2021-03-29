import logging

import coloredlogs
import verboselogs

from utils.exception import to_str

# FIXME DEBUG level not working


class Log:
    """Wrapper class for coloured and verbuse logs."""

    levels = {}
    default = None

    @classmethod
    def init(cls, default, levels):
        """Set the default and levels and initialize the log manager.

        :param cls: Log class.
        :param default: default log level
        :param levels: log levels
        """
        verboselogs.install()
        coloredlogs.install()
        cls.default = default
        cls.levels = {module: level for module, level in levels}
        logging.get_logger = logging.getLogger
        for module, level in levels:
            logging.get_logger(module).setLevel(level)

    @classmethod
    def get(cls, name):
        """Return the initialized logger with the module name.

        :param cls: Log class.
        :param name: module name
        :returns: logger instance
        """
        level = cls.levels.get(name, cls.default)
        logger = logging.get_logger(name)

        def __exception(message, exception):
            logger.error(message)
            logger.debug(to_str(exception))
        logger.exception = __exception

        logger.setLevel(level)
        return logger

    @staticmethod
    def get_levels():
        """Get list of log level names.

        :returns: list of string
        """
        return logging._levelToName.values()
