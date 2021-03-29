from functools import partial
from xml.parsers.expat import ExpatError as Expat_Error

import xmltodict as xml_to_dict
import yaml
from dicttoxml import dicttoxml as dict_to_xml
from falcon.errors import HTTPBadRequest as HTTP_Bad_Request
from falcon.media import JSONHandler as JSON_Handler
from yaml import FullLoader as Full_Loader
from yaml.parser import ParserError as Parser_Error
from yaml.parser import ScannerError as Scanner_Error


class XML_Handler(JSON_Handler):
    def __init__(self, dumps=None, loads=None):
        self.dumps = dumps or partial(dict_to_xml, custom_root='astrid', attr_type=False)
        self.loads = loads or partial(xml_to_dict.parse, force_list='item')

    def deserialize(self, stream, content_type, content_length):
        try:
            return self.loads(stream.read().decode('utf-8'))['astrid']
        except Expat_Error:
            raise HTTP_Bad_Request('Invalid XML')


class YAML_Handler(JSON_Handler):
    def __init__(self, dumps=None, loads=None):
        self.dumps = dumps or partial(yaml.dump, sort_keys=True, indent=3)
        self.loads = loads or partial(yaml.load, Loader=Full_Loader)

    def deserialize(self, stream, content_type, content_length):
        try:
            x = stream.read().decode('utf-8')
            return self.loads(x)
        except (Parser_Error, Scanner_Error):
            raise HTTP_Bad_Request('Invalid YAML')
