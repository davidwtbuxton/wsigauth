import unittest
from wsgiref.simple_server import make_server

import webtest

import wsgiauth


def test_app(environ, start_response):
    start_response('200 OK', [('content-type', 'text/plain')])
    return ['OK']


class AuthMiddlewareTestCase(unittest.TestCase):
    def test_no_auth_middleware(self):
        app = webtest.TestApp(test_app)

        response = app.get('/')

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, 'OK')

    def test_basic_auth_allow(self):
        auth_app = wsgiauth.AuthMiddleware(test_app, basic=('alice', 'secret'))
        app = webtest.TestApp(auth_app)

        app.authorization = ('Basic', ('alice', 'secret'))
        response = app.get('/')

        self.assertEqual(response.status_int, 200)

    def test_basic_auth_deny_no_password(self):
        auth_app = wsgiauth.AuthMiddleware(test_app, basic=('alice', 'secret'))
        app = webtest.TestApp(auth_app)

        response = app.get('/', status=401)

        self.assertEqual(response.status_int, 401)

    def test_basic_auth_deny_wrong_password(self):
        auth_app = wsgiauth.AuthMiddleware(test_app, basic=('alice', 'secret'))
        app = webtest.TestApp(auth_app)

        app.authorization = ('Basic', ('alice', 'wrong-password'))
        response = app.get('/', status=401)

        self.assertEqual(response.status_int, 401)
