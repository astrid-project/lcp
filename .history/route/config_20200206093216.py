from datetime import datetime
from marshmallow import fields, Schema
import falcon
import subprocess



class ConfigResource(object):
    request_schema = ConfigRequestSchema()
    response_schema = ConfigResponseSchema()

