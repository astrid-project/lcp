from configparser import BasicInterpolation
from os import path


class EnvInterpolation(BasicInterpolation):
    """
    Interpolation which expands environment variables in values.
    """

    def before_get(self, parser, section, option, value, defaults):
        """
        Executes before getting the value.

        :param self: class instance
        :param parser: configparser instance
        :param section: section value
        :param option: option value
        :param value: current value
        :param defaults: default values
        :returns value with expanded variables
        """
        return path.expandvars(value)
