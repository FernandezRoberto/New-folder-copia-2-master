from google.appengine.ext import db
#from Encryption import Encript
from google.appengine.ext.blobstore import blobstore
import logging

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class DictModel(db.Model):
    def to_dict(self):
       resp =  dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       resp['id'] = self.key().id()
       return resp

class User(DictModel):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    username = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    tipoUsuario = db.StringProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)
    deleted = db.BooleanProperty(required = True, default = False)

    @classmethod
    def by_id(cls, uid):
        user = User.get_by_id(uid, parent = users_key())
        if user:
            return user.to_dict()
        else:
            return None

    @classmethod
    def by_id_instance(cls, uid):
        user = User.get_by_id(uid, parent = users_key())
        if user:
            return user
        else:
            return None

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM User where deleted = False")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def get_username(cls, username):
        res = db.GqlQuery("SELECT * FROM User where isDeleted = False AND username = :1",username)
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def get_email(cls, email):
        res = db.GqlQuery("SELECT * FROM User where isDeleted = False AND email = :1",email)
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def by_username(cls, username):
        u = User.all().filter('username =', username).get()
        return u
       
    @classmethod
    def by_email(cls, email):
        u = User.all().filter('email =', email).get()
        return u

    @classmethod
    def editUser(cls, id, nombre, apellido, username, tipoUsuario):
        user = cls.by_id_instance(id)
        user.first_name = nombre
        user.last_name = apellido
        user.username = username
        user.tipoUsuario = tipoUsuario
        user.put()

    @classmethod
    def deleteUser(cls,id):
        user = cls.by_id_instance(id)
        user.deleted = True
        user.put()

    @classmethod
    def register(cls, first_name, last_name, username, email, password, tipoUsuario):
        #pw_hash = enc.make_pw_hash(username, password)
        return User(parent = users_key(),
                    first_name = first_name, 
                    last_name = last_name,
                    username = username, 
                    email = email, 
                    #confirmation = confirmation, 
                    password = password, #pw_hash,
                    tipoUsuario = tipoUsuario,
                    deleted = False)

    @classmethod
    def login(cls, username, password):
        u = cls.by_username(username)
        if u:
            #if not u.confirmation == "confirmed":
            #    return None
            #if enc.valid_pw(username, password, u.password):
            if(u.password == password):
                return u
            else:
                return None
            #if password == u.password:
            #    return u