#!/usr/bin/env python

import logging
import os.path

import tornado.ioloop
import tornado.web
import tornado.httpserver

from articles.handlers import (
    MainHandler, ListArticlesHandler, AuthLoginHandler, AuthLogoutHandler
)
from articles.settings import settings


class Application(tornado.web.Application):

    def __init__(self):
        app_settings = {
            'cookie_secret': settings['cookie_secret'],
            'xsrf_cookies': True,
            'debug': settings['debug'],
            'template_path': os.path.join(
                os.path.dirname(__file__), 'templates'),
            'facebook_app_id': settings['facebook']['client_id'],
            'facebook_secret': settings['facebook']['client_secret']
        }

        routes = [
            (r'/', MainHandler),
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
            (r'/articles', ListArticlesHandler),
        ]

        super(Application, self).__init__(routes, **app_settings)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True
    )
    server.listen(settings['port'], address=settings['address'])
    logging.debug('App listen on {}:{}'.format(settings['address'],
                                               settings['port']))
    tornado.ioloop.IOLoop().current().start()