from apispec import APISpec as API_Spec
from apispec.ext.marshmallow import MarshmallowPlugin as Marshmallow_Plugin
from falcon_apispec import FalconPlugin as Falcon_Plugin
from json import dumps
from pathlib import Path
from resource import tags as rc_tags
from utils.string import is_str

__all__ = [
    'Spec'
]


class Spec:
    def __init__(self, api, title, version):
        self.obj = API_Spec(title=title, version=version, openapi_version='2.0',
                            produces=['application/json'], consumes=['application/json'],
                            tags=rc_tags, plugins=[Falcon_Plugin(api), Marshmallow_Plugin(schema_name_resolver=self.__schema_name_resolver)])

    def get(self):
        return self.obj

    def write(self):
        path = Path(__file__).parent / '../swagger/schema.yaml'
        with path.open('w') as file:
            file.write(self.obj.to_yaml())
        path = Path(__file__).parent / '../swagger/schema.json'
        with path.open('w') as file:
            file.write(dumps(self.obj.to_dict(), indent=2))

    @staticmethod
    def __schema_name_resolver(schema):
        if is_str(schema):
            ref = schema
        else:
            ref = schema.__class__.__name__
        return ref.replace('_Schema', '')
