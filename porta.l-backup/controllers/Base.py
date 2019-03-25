import webapp2
import os
import jinja2
from google.appengine.api import memcache
import logging

template_dir = os.path.join(os.path.dirname(__file__), '..', 'views')
jinja_envAutoEscape = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class BaseHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_envAutoEscape.get_template(template)
        return t.render(params)

    def render_str2(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def renderNoEscape(self, template, **kw):
        self.write(self.render_str2(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = val
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val

    def init(self):
        self.params['user_id'] = self.read_secure_cookie("user_id")
        #query que recupere del user dado su user id
        # 0 -> Redireccionar al login
        # 1 -> self.params['user']  -> objecto del usario
        self.params['username'] = self.read_secure_cookie("username")
        self.params['tipo'] = self.read_secure_cookie("tipo")

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
        self.set_secure_cookie('username', str(user.username))
        self.set_secure_cookie('tipo', str(user.tipoUsuario))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.response.headers.add_header('Set-Cookie', 'tipo=; Path=/')

    def initialize(self, *a, **kw):
        self.params = dict()
        self.params['username'] = None
        self.params['tipo'] = None
        self.params['Current'] = 'Index'
        webapp2.RequestHandler.initialize(self, *a, **kw)

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))
