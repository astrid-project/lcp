from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_apispec import FalconPlugin
from json import dumps
from resource import tags as rc_tags


class Spec:
    def __init__(self, api, title, version):
        self.obj = APISpec(title=title, version=version,
            openapi_version='2.0',
            produces=['application/json'], consumes=['application/json'],
            tags=rc_tags,
            plugins=[ FalconPlugin(api), MarshmallowPlugin() ],
        )

    def get(self):
        return self.obj

    def write(self):
        with open('./swagger/schema.yaml', 'w') as file: file.write(self.obj.to_yaml())
        with open('./swagger/schema.json', 'w') as file: file.write(dumps(self.obj.to_dict(), indent=2))
