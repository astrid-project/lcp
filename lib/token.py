from datetime import datetime, timedelta

import jwt

from reader import Arg_Reader


def create_token():
    now = datetime.now()
    exp = now + timedelta(minutes=10)
    payload = {'iat': now.timestamp(), 'exp': exp.timestamp(), 'nbf': now.timestamp()}
    token = jwt.encode(payload, Arg_Reader.db.auth_secret_key)
    return f'{Arg_Reader.db.auth_header_prefix} {token}'
