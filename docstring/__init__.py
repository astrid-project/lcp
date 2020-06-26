from pathlib import Path

__all__ = [
    'docstring'
]


def docstring(source):
    """Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def decorator(self):
        path = Path(__file__).parent / f'../docstring/{source}'
        with path.open('r') as file:
            self.__doc__ = file.read()
        return self
    return decorator
