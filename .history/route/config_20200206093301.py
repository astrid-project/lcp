from datetime import datetime
from schema import ConfigRequest, ConfigResponse
import falcon
import subprocess


class ConfigResource(object):
    request_schema = ConfigRequest()
    response_schema = ConfigResponse()
