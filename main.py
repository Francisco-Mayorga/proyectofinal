#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message
from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')

            params = {"activo": "/", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/')

            params = {"activo": "/", "logged_in": logged_in, "login_url": login_url, "user": user}

        return self.render_template("index.html", params)

class EnviadosHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/enviados')

            enviados = {"activo": "enviados", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/enviados')

            enviados = {"activo": "enviados", "logged_in": logged_in, "login_url": login_url, "user": user}

        return self.render_template("enviados.html", params=enviados)

class RecibidosHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/recibidos')

            recibidos = {"activo": "recibidos", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/recibidos')

            recibidos = {"activo": "recibidos", "logged_in": logged_in, "login_url": login_url, "user": user}

        return self.render_template("recibidos.html", params=recibidos)

class NuevoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/nuevo-mensaje')

            nuevomensaje = {"activo": "nuevo-mensaje", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/enviados')

            nuevomensaje = {"activo": "nuevo-mensaje", "logged_in": logged_in, "login_url": login_url, "user": user}

        return self.render_template("nuevo-mensaje.html", params=nuevomensaje)

class TiempoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/el-tiempo')

            eltiempo = {"activo": "el-tiempo", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/el-tiempo')

            eltiempo = {"activo": "el-tiempo", "logged_in": logged_in, "login_url": login_url, "user": user}

        return self.render_template("el-tiempo.html", params=eltiempo)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/enviados', EnviadosHandler),
    webapp2.Route('/recibidos', RecibidosHandler),
    webapp2.Route('/nuevo-mensaje', NuevoHandler),
    webapp2.Route('/el-tiempo', TiempoHandler),
], debug=True)
