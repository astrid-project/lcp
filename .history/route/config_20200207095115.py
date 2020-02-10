from .base import BaseResource
from datetime import datetime
from schema import ConfigRequest, ConfigResponse
import falcon
import subprocess


class ConfigResource(BaseResource):
    request_schema = ConfigRequest()
    response_schema = ConfigResponse()

    route = ['/config']
