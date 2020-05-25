from marshmallow import Schema
from marshmallow.fields import List, String


class ConfigParameterRequestSchema(Schema):
    """
    Parameter part in a single item of the code request.
    """
    scheme = String(required=True, description='Scheme.', choice=['json', 'yaml', 'ini'], example='yaml')
    source = String(required=True, description='Source filename.', example='filebeat.yml')
    path = List(String(required=True, description='Path item.', example='period'), description='Key path')
    value = String(required=True, description='Parameter new value.', example='10s')
