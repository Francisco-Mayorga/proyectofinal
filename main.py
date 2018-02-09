#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Message
from google.appengine.api import users
from models import User
import json
from google.appengine.api import urlfetch


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
            user_db = User.get_by_user(user)
            if not user_db:
                new_user_db = User(user_id=user.user_id(), nickname=user.user_id())
                new_user_db.put()
            logged_in = True
            logout_url = users.create_logout_url('/')

            params = {"activo": "/", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/')

            params = {"activo": "/", "logged_in": logged_in, "login_url": login_url, "user": user}

        data = open("people.json", "r").read()
        json_data = json.loads(data)

        params["people_list"] = json_data

        return self.render_template("index.html", params)

class EnviadosHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_db = User.get_by_user(user)
            if not user_db:
                new_user_db = User(user_id=user.user_id(), nickname=user.user_id())
                new_user_db.put()

            logged_in = True
            logout_url = users.create_logout_url('/')

            enviados = {"activo": "enviados", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")

        messages = Message.query(Message.deleted == False, Message.sender == user.user_id()).fetch()
        enviados["messages"] = messages
        return self.render_template("enviados.html", params=enviados)



class RecibidosHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_db = User.get_by_user(user)
            if not user_db:
                new_user_db = User(user_id=user.user_id(), nickname=user.user_id())
                new_user_db.put()

            logged_in = True
            logout_url = users.create_logout_url('/')

            recibidos = {"activo": "recibidos", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")

        messages = Message.query(Message.deleted == False, Message.receiver == user.user_id()).fetch()
        recibidos["messages"] = messages
        return self.render_template("recibidos.html", params=recibidos)

class NuevoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')


            nuevomensaje = {"activo": "nuevo-mensaje", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")

        return self.render_template("nuevo-mensaje.html", params=nuevomensaje)

    def post(self):
        user = users.get_current_user()

        # get inputs values
        asunto = self.request.get("asunto")
        texto = self.request.get("texto")
        email = user.email()

        if not asunto:
            asunto = u"anónimo"

        new_message = Message(asunto=asunto, texto=texto, email=email, sender=user.user_id(), receiver=user.user_id())
        new_message.put()

        return self.redirect_to('enviados')

class TiempoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')

            eltiempo = {"activo": "el-tiempo", "logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")


        url = "http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric&appid=4f6c7a15fb1b6fc272b05225a0e4bcb9"

        response = urlfetch.fetch(url)
        data = response.content
        weather_info = json.loads(data)

        eltiempo["weather_info"] = weather_info


        return self.render_template("el-tiempo.html", params=eltiempo)

class DetallesHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')

            detalles = {"logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")

        message = Message.get_by_id(int(message_id))
        detalles["message"] = message
        return self.render_template("detallesmensajes.html", params=detalles)

class EditarHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')

            editar = {"logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")

        message = Message.get_by_id(int(message_id))
        editar["message"] = message
        return self.render_template("editarmensaje.html", params=editar)

    def post(self, message_id):
        asunto = self.request.get("asunto")
        email = self.request.get("email")
        texto = self.request.get("texto")
        message = Message.get_by_id(int(message_id))
        message.asunto = asunto
        message.email = email
        message.texto = texto
        message.put()
        return self.redirect_to("enviados")

class BorrarHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')

            borrar = {"logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            return self.redirect_to("index")

        message = Message.get_by_id(int(message_id))
        borrar["message"] = message
        return self.render_template("borrarmensaje.html", params=borrar)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.deleted = True
        message.put()
        return self.redirect_to("enviados")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="index"),
    webapp2.Route('/enviados', EnviadosHandler, name="enviados"),
    webapp2.Route('/message/<message_id:\d+>/detalles', DetallesHandler),
    webapp2.Route('/message/<message_id:\d+>/editar', EditarHandler),
    webapp2.Route('/message/<message_id:\d+>/borrar', BorrarHandler),
    webapp2.Route('/recibidos', RecibidosHandler),
    webapp2.Route('/nuevo-mensaje', NuevoHandler),
    webapp2.Route('/el-tiempo', TiempoHandler),
], debug=True)
