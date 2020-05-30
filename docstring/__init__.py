def docstring(source):
    """
    Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def decorator(self, **params):
        with open(f'./docstring/{source}', 'r') as file:
            self.__doc__ = file.read().format(**params)
        return self
    return decorator
