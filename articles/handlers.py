
import os.path
import ujson
import logging

import tornado.web
import tornado.auth
import tornado.escape
import tornado.gen

from articles.template_render import TemplateRenderer


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.render_article = TemplateRenderer(
            path=os.path.join(self.settings['template_path'], 'articles')
        )

    @property
    def db(self):
        return self.application.database

    def get_current_user(self):
        user = self.get_secure_cookie('fbuser')
        if not user:
            return None
        return ujson.loads(user)


class JSONHandler(BaseHandler):

    def set_default_headers(self):
        super(BaseHandler, self).set_default_headers()
        self.set_header('Content-Type', 'application/json')


class MainHandler(BaseHandler):

    async def get(self):
        self.render('login.html')


class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):

    @tornado.web.asynchronous
    def get(self):

        url = '{}://{}/auth/login?next={}'.format(
            self.request.protocol, self.request.host,
            tornado.escape.url_escape('/')
        )

        if self.get_argument('code', False):
            self.get_authenticated_user(
                redirect_uri=url,
                client_id=self.settings['facebook_app_id'],
                client_secret=self.settings['facebook_secret'],
                code=self.get_argument('code'),
                callback=self._on_auth
            )
            return
        scope = ','.join([
            'pages_manage_instant_articles',
            'manage_pages',
            'pages_show_list',
            'user_managed_groups'
        ])

        return self.authorize_redirect(
            redirect_uri=url,
            client_id=self.settings['facebook_app_id'],
            client_secret=self.settings['facebook_secret'],
            extra_params={'scope': scope}
        )

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, 'Authentication failed')
        self.set_secure_cookie('fbuser', ujson.dumps(user))
        self.redirect(self.get_argument('next', '/'))


class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):

    async def get(self):
        self.clear_cookie('fbuser')
        self.redirect('/')


class ArticlesHandler(JSONHandler, tornado.auth.FacebookGraphMixin):

    # @tornado.web.authenticated
    async def get(self):

        data = await self.render_article('test.html', name='Ivan')
        # accounts = await self.facebook_request(
        #     '/me/accounts',
        #     access_token=self.current_user['access_token']
        # )
        # logging.debug(accounts)
        self.write(data)

    @tornado.web.authenticated
    async def post(self):
        self.write('Article posted')
