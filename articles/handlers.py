import ujson
import logging
import tornado.web
import tornado.auth
import tornado.escape
import tornado.gen


class BaseHandler(tornado.web.RequestHandler):

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
    async def get(self):

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
        return self.authorize_redirect(
            redirect_uri=url,
            client_id=self.settings['facebook_app_id'],
            client_secret=self.settings['facebook_secret'],
            extra_params={'scope': 'user_posts'})

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError('Authentication failed')
        self.set_secure_cookie('fbuser', ujson.dumps(user))
        self.redirect(self.get_argument('next', '/'))


class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):

    async def get(self):
        self.clear_cookie('fbuser')
        self.redirect('/')


class ListArticlesHandler(JSONHandler):

    async def get(self):
        payload = ujson.dumps({
            'articles': [
                {
                    'message': 'test message 1'
                },
                {
                    'message': 'Link test'
                }
            ]
        })
        self.write(payload)
