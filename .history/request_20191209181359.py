from flask import request as request_flask


class Request:
    @staticmethod
    def json(error):
        try:
            return request_flask.json
        except:
            value = request_flask.data
            if len(value) == 0:
                return {}
            else:
                error(message='Not acceptable value',
                      what='request', value=value.decode('utf-8'))
