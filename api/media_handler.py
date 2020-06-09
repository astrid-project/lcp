from falcon import errors
from falcon.media import JSONHandler
from functools import partial

#import lazyxml
import yaml


class XMLHandler(JSONHandler):
    # def __init__(self, dumps=None, loads=None):
        #self.dumps = dumps or lazyxml.dumps
        #self.loads = loads or lazyxml.loads

    def deserialize(self, stream, content_type, content_length):
        try:
            return self.loads(stream.read().decode('utf-8'))
        except ValueError as err:
            raise errors.HTTPBadRequest('Invalid XML',
                                        f'Could not parse XML body - {err}')


class YAMLHandler(JSONHandler):
    def __init__(self, dumps=None, loads=None):
        self.dumps = dumps or partial(yaml.dump, sort_keys=True, indent=3)
        self.loads = loads or partial(yaml.load, Loader=yaml.FullLoader)

    def deserialize(self, stream, content_type, content_length):
        try:
            x = stream.read().decode('utf-8')
            return self.loads(x)
        except yaml.parser.ParserError as err:
            raise errors.HTTPBadRequest('Invalid YAML',
                                        f'Could not parse YAML body - {err}')
