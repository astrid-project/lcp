from error.http_not_valid_json import HTTPNotValidJSON
from jproperties import Properties
from resource.base import BaseResource
from schema.config.request import ConfigRequestSchema
from schema.config.response import ConfigResponseSchema
from schema.http_error import HTTPErrorSchema
from utils.datetime import datetime_to_str
from utils.docstring import docstring
from utils.sequence import wrap


class ConfigResource(BaseResource):
    request_schema = ConfigRequestSchema()
    response_schema = ConfigResponseSchema()
    daemon_pids = {}
    tag = dict(name='config', description='Configuration at run-time.')
    routes = '/config',
    history_filename = 'data/config.history'

    @docstring(source='config/get.yaml')
    def on_get(self, req, resp):
        req.context['result'] = self.history

    from resource.config.actions import make_actions
    from resource.config.parameters import make_parameters
    from resource.config.resources import make_resources

    @docstring(source='config/post.yaml')
    def on_post(self, req, resp):
        data = req.context.get('json', None)
        if data is not None:
            res = dict(when=datetime_to_str(), results=[])
            for config in wrap(data):
                for cfg, cfg_list in config.items():
                    for data in wrap(cfg_list):
                        if cfg == 'actions':
                            output = self.make_actions(data)
                        elif cfg == 'parameters':
                            output = self.make_parameters(data)
                        elif cfg == 'resources':
                            output = self.make_resources(data)
                        else:
                            output = dict(type=cfg, error=True, description='Request type unknown')
                        res['results'].append(output)
            req.context['result'] = res
            self.history.append(res)
        else:
            raise HTTPNotValidJSON()
