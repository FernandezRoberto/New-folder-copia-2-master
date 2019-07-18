from Base import BaseHandler
import jinja2
import os
import logging
import webapp2
import json

from models.User import User

class UserLogin(BaseHandler):
    def post(self): 
        user = User.login(self.request.get('username'),self.request.get('pass'))
        if (user != None):
            self.login(user)
            self.redirect('/')
        else:
            self.params['loginError'] = "Nombre de Usuario o Contrasenia incorrecto"
            self.render('users/login.html', **self.params)

    def get(self):
        self.init()
        usersCant = User.get_all();
        if (len(usersCant) == 0):
            user = dict(
              nombre = "Administrador",
              apellido =  "Administrador",
              username = "Administrador",
              correo = "administrador@administrador.com",
              passw = "@Admin@",
              tipoUsuario = "Administrador"
            )
            n = User.register(user['nombre'], user['apellido'], user['username'], user['correo'], user['passw'], user['tipoUsuario'])
            n.put()  
            uid = self.read_secure_cookie("username")
            if uid:
                self.params['username'] = uid
            self.render('users/login.html', **self.params)
        else:
            uid = self.read_secure_cookie("username")
            if uid:
                self.params['username'] = uid
            self.render('users/login.html', **self.params)

class UserLogout(BaseHandler):
    def get(self):
        self.logout()
        self.render('index.html', **self.params)

class CreateUser(BaseHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        user = dict(
          nombre = user_json.get("nombre", "").strip(),
          apellido = user_json.get("apellido", "").strip(),
          username = user_json.get("username", "").strip(),
          correo = user_json.get("correo", "").strip(),
          passw = user_json.get("pass", "").strip(),
          tipoUsuario = user_json.get("tipoUsuario","").strip()
        )

        usernameValid = User.get_username(user['username']);
        emailValid = User.get_email(user['correo']);
        if (len(usernameValid) == 0 and len(emailValid) == 0):
          n = User.register(user['nombre'], user['apellido'], user['username'], user['correo'], user['passw'], user['tipoUsuario'])
          n.put()
          #self.render('index.html', **self.params)
          self.response.headers['Content-Type'] = 'application/json'   
          #obj = {
           # 'url': '/user/show', 
            #'message': 'Usuario registrado con exito',
          #} 
          #self.response.status = 200
          response = { 'message': user['nombre']+' '+user['apellido']+ ' registrado con exito', 'redirect_url': '/user/show' }
          self.response.out.write(json.dumps(response))
          #return webapp2.redirect('/user/login')
        else:
          self.response.headers['Content-Type'] = 'application/json'   
          response = { 'message': 'El Usuario: '+user['nombre']+' '+user['apellido']+' ya existe, ingrese otro usuario y/o correo', 'redirect_url': '/user/register'}
          self.response.out.write(json.dumps(response))

    def get(self):
        self.init()
        self.params['post_url'] = '/user/register'
        self.render('users/register.html', **self.params)

class EditUser(BaseHandler):

    def post(self, note_id):
        iden = int(note_id)
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        user = dict(
          iden = iden,
          nombre = user_json.get("nombre", "").strip(),
          apellido = user_json.get("apellido", "").strip(),
          username = user_json.get("username", "").strip(),
          correo = user_json.get("correo", "").strip(),
          passw = user_json.get("pass", "").strip(),
          tipoUsuario = user_json.get("tipoUsuario","").strip()
        )
        User.editUser(user['iden'], user['nombre'], user['apellido'], user['username'], user['tipoUsuario'])
        #User.editUser(iden,self.request.get('nombre'),self.request.get('apellido'),self.request.get('username'),self.request.get('tipoUsuario'))
        self.response.headers['Content-Type'] = 'application/json'   
        response = { 'message': user['nombre'] + ' modificado con exito', 'redirect_url': '/user/show' }
        self.response.out.write(json.dumps(response))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        user = User.by_id(iden)
        self.params['user'] = user
        self.render('users/editUser.html', **self.params)
        #self.render_template('users/editUser.html', {'user': user},)

class DeleteUser(BaseHandler):

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        User.deleteUser(iden)
        return webapp2.redirect('/')

class ShowUsers(BaseHandler):

    def get(self):
        self.init()
        users = User.get_all();
        self.params['users'] = users
        self.render('users/listUsers.html', **self.params)
        
