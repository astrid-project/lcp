from marshmallow.fields import List
from utils.sequence import wrap

__all__ = [
    'List_or_One'
]


class List_or_One(List):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            if isinstance(value, str):
                value = value.replace('\r', '').splitlines();
            else:
                value = wrap(value)
        return super(List_or_One, self)._deserialize(value, attr, data, **kwargs)
