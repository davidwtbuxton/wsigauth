WSGI Auth Middleware
====================

Simple Python WSGI middleware you can use to wrap your application with HTTP basic authentication. Intended for hiding a site behind a simple name and password.

Usage
-----

Wrap your wsgi application object with AuthMiddleware. Here's an example using Bottle:

    import bottle
    import wsgiauth

    app = bottle.default_app()

    @app.route('/')
    def home():
        return 'Hello, world!'

    if __name__ == '__main__':
        app = wsgiauth.AuthMiddleware(app, basic=('alice', 'secret'))
        app.run()

Another example using Django - this would go in your wsgi.py:

    import os

    import wsgiauth
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    application = get_wsgi_application()
    application = wsgiauth.AuthMiddleware(application, basic=('alice', 'secret'))
