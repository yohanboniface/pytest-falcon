import json

import pytest
from falcon.testing.helpers import create_environ
from falcon.testing.srmock import StartResponseMock

try:
    from urllib.parse import urlparse, urlencode
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode


class Client(object):

    def __init__(self, app, **kwargs):
        self.app = app
        self._before = kwargs.get('before')
        self._after = kwargs.get('after')

    def __call__(self, app=None, **kwargs):
        return Client(app or self.app, **kwargs)

    def encode_body(self, kwargs):
        body = kwargs.get('body')
        headers = kwargs.get('headers')
        content_type = headers.get('Content-Type')
        if not body or not content_type or isinstance(body, str):
            return
        if 'application/x-www-form-urlencoded' in content_type:
            kwargs['body'] = urlencode(body)
        elif 'application/json' in headers['Content-Type']:
            kwargs['body'] = json.dumps(body)

    def fake_request(self, path, **kwargs):
        kwargs.setdefault('headers', {})
        if self._before:
            self._before(kwargs)
        parsed = urlparse(path)
        path = parsed.path
        if parsed.query:
            kwargs['query_string'] = parsed.query
        self.encode_body(kwargs)
        resp = StartResponseMock()
        body = self.app(create_environ(path, **kwargs), resp)
        resp.headers = resp.headers_dict
        resp.status_code = int(resp.status.split(' ')[0])
        resp.body = body[0].decode() if body else ''
        if 'application/json' in resp.headers.get('Content-Type', ''):
            resp.json = json.loads(resp.body) if resp.body else {}
        if self._after:
            self._after(resp)
        return resp

    def get(self, path, **kwargs):
        return self.fake_request(path, method='GET', **kwargs)

    def post(self, path, data, **kwargs):
        kwargs.setdefault('headers', {})
        headers = kwargs['headers']
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return self.fake_request(path, method='POST', body=data, **kwargs)

    def put(self, path, body, **kwargs):
        return self.fake_request(path, method='PUT', body=body, **kwargs)

    def patch(self, path, body, **kwargs):
        return self.fake_request(path, method='PATCH', body=body, **kwargs)

    def delete(self, path, **kwargs):
        return self.fake_request(path, method='DELETE', **kwargs)

    def before(self, func):
        self._before = func

    def after(self, func):
        self._after = func


@pytest.fixture
def client(app):
    return Client(app)
