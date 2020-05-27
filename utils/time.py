from pint import UnitRegistry


ureg = UnitRegistry()
Q_ = ureg.Quantity


def get_seconds(text, to_int=False):
    """
    Parse the text to get the equivalent number of seconds (e.g., 1min => 60).

    :params text: input time in human format, e.g.: 1m
    :params to_int: convert to int the result
    :returns: number of seconds
    """
    n = (Q_(text).to(ureg.second)).magnitude
    return int(n) if to_int else n
