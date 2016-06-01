#!/usr/bin/env python

import logging
import os.path

import peewee_async
import tornado.ioloop
import tornado.web
import tornado.httpserver

from articles.handlers import (
    MainHandler, ArticlesHandler, AuthLoginHandler, AuthLogoutHandler
)
from articles.settings import settings


BASE_DIR = os.path.dirname(__file__)


class Application(tornado.web.Application):

    def __init__(self):
        app_settings = {
            'cookie_secret': settings['cookie_secret'],
            'xsrf_cookies': True,
            'debug': settings['debug'],
            'template_path': os.path.join(BASE_DIR, 'templates'),
            'facebook_app_id': settings['facebook']['client_id'],
            'facebook_secret': settings['facebook']['client_secret']
        }

        routes = [
            (r'/', MainHandler),
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
            (r'/articles', ArticlesHandler),
        ]

        self.database = peewee_async.PooledPostgresqlDatabase(
            settings['postgres']['database'],
            user=settings['postgres']['username'],
            host=settings['postgres']['host']
        )

        super(Application, self).__init__(routes, **app_settings)


def main():
    server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True
    )
    server.listen(settings['port'], address=settings['address'])
    logging.debug('App listen on {}:{}'.format(settings['address'],
                                               settings['port']))
    tornado.ioloop.IOLoop().current().start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
