from marshmallow.fields import List

__all__ = [
    'List_or_One'
]


class List_or_One(List):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            if isinstance(value, str):
                value = [value]
            elif isinstance(value, self.inner):
                value = value.replace('\r', '').splitlines();
        return super(List_or_One, self)._deserialize(value, attr, data)
