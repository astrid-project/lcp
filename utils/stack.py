from inspect import getframeinfo, stack


def info(level):
    return getframeinfo(stack()[level][0])
