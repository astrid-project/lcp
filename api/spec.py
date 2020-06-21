from apispec import APISpec as API_Spec
from apispec.ext.marshmallow import MarshmallowPlugin as Marshmallow_Plugin
from falcon_apispec import FalconPlugin as Falcon_Plugin
from json import dumps
from resource import tags as rc_tags

__all__ = [
    'Spec'
]


class Spec:
    def __init__(self, api, title, version):
        self.obj = API_Spec(title=title, version=version, openapi_version='2.0',
                            produces=['application/json'], consumes=['application/json'],
                            tags=rc_tags,    plugins=[Falcon_Plugin(api), Marshmallow_Plugin()])

    def get(self):
        return self.obj

    def write(self):
        with open('./swagger/schema.yaml', 'w') as file:
            file.write(self.obj.to_yaml())
        with open('./swagger/schema.json', 'w') as file:
            file.write(dumps(self.obj.to_dict(), indent=2))
