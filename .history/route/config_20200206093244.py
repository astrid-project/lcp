from datetime import datetime
from schema import
import falcon
import subprocess


class ConfigResource(object):
    request_schema = ConfigRequestSchema()
    response_schema = ConfigResponseSchema()

