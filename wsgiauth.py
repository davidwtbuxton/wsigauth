class AuthMiddleware(object):
    def __init__(self, app, basic):
        """`basic` is a tuple of (<name>, <password>) to use for basic auth."""
        self.app = app
        self.basic = basic

    def __call__(self, environ, start_response):
        try:
            auth = environ['HTTP_AUTHORIZATION']
            scheme, data = auth.split(None, 1)
            assert scheme.lower() == 'basic'
            username, password = data.decode('base64').split(':', 1)
            assert (username, password) == self.basic
        except (KeyError, AssertionError):
            return access_denied(environ, start_response)

        return self.app(environ, start_response)


def access_denied(environ, start_response):
    headers = [('WWW-Authenticate', 'Basic realm="private"')]
    start_response('401 Unauthorized', headers)

    return ['Unauthorized']
