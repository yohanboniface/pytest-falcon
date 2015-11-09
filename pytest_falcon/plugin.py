import json
from urllib import parse

import pytest
from falcon.testing.srmock import StartResponseMock
from falcon.testing.helpers import create_environ


class Client(object):

    def __init__(self, app):
        self.app = app

    def fake_request(self, path, **kwargs):
        parsed = parse.urlparse(path)
        path = parsed.path
        if parsed.query:
            kwargs['query_string'] = parsed.query
        resp = StartResponseMock()
        body = self.app(create_environ(path, **kwargs), resp)
        resp.headers = resp.headers_dict
        resp.status_code = int(resp.status.split(' ')[0])
        resp.body = body[0].decode() if body else ''
        if 'application/json' in resp.headers.get('Content-Type', ''):
            resp.json = json.loads(resp.body)
        return resp

    def get(self, path, **kwargs):
        return self.fake_request(path, method='GET', **kwargs)

    def post(self, path, data, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
        body = parse.urlencode(data)
        return self.fake_request(path, method='POST', body=body, **kwargs)

    def put(self, path, body, **kwargs):
        return self.fake_request(path, method='PUT', body=body, **kwargs)


@pytest.fixture
def client(app):
    return Client(app)
