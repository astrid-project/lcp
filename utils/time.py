from pint import UnitRegistry as Unit_Registry

__all__ = [
    'get_seconds'
]

__ureg = Unit_Registry()
__Q = __ureg.Quantity


def get_seconds(text, to_int=False):
    """Parse the text to get the equivalent number of seconds (e.g., 1min => 60).

    :params text: input time in human format, e.g.: 1m
    :params to_int: convert to int the result
    :returns: number of seconds
    """
    n = (__Q(text).to(__ureg.second)).magnitude
    return int(n) if to_int else n
