from datetime import datetime
from utils.datetime import datetime_from_str, datetime_to_str
from utils.docstring import docstring


@docstring(source='status/post.yaml')
def on_post(self, req, resp):
    data = req.context.get('json', {})
    id = data.get('id', None)
    self.data['id'] = id
    cb_expiration = data.get('cb_expiration', None)
    self.cb = dict(password=data.get('cb_password', None), expiration=cb_expiration,
                    host=req.host, port=req.port)
    username = data.get('username', None) # FIXME how to send username the first connection
    password = data.get('password', None)
    if username and self.auth_db.get(username, None) != hash(password):
        raise HTTPUnauthorized(dict(title='401 Unauthorized', description='Invalid Username/Password'))
    if not username:
        username = generate_username()
    password = generate_password()
    self.auth_db[username] = hash(password)
    # FIXME set_ttl
    # self.auth_db.set_ttl(username, (datetime_from_str(cb_expiration) - datetime.now()).total_seconds())
    if id is not None:
        now = datetime_to_str()
        self.data['last_hearthbeat'] = now
        if ArgReader.db.log_level == 'DEBUG':
            self.log.notice(f'Hearbeating from CB at {now} (password: {self.cb.get("password", None)} - expiration: {self.cb. get("expiration", None)})')
        else:
            self.log.notice(f'Hearbeating from CB at {now}')
    req.context['result'] = dict(**self.data, username=username, password=password)
