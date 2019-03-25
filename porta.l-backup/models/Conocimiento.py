from google.appengine.ext import db
#from Encryption import Encript
from google.appengine.ext.blobstore import blobstore
import logging

def conocimientos_key(group = 'default'):
    return db.Key.from_path('conocimientos', group)

class DictModel(db.Model):
    def to_dict(self):
       resp =  dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       resp['id'] = self.key().id()
       return resp

class Conocimiento(DictModel):
    descripcion = db.StringProperty(required = True)
    categoria = db.StringProperty(required = True)
    explicacion = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    isDeleted = db.BooleanProperty(required = True, default = False)

    @classmethod
    def by_id(cls, uid):
        conocimiento = Conocimiento.get_by_id(uid, parent = conocimientos_key())
        if conocimiento:
            return conocimiento.to_dict()
        else:
            return None

    @classmethod
    def by_id_instance(cls, uid):
        conocimiento = Conocimiento.get_by_id(uid, parent = conocimientos_key())
        if conocimiento:
            return conocimiento
        else:
            return None

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM Conocimiento where isDeleted = False")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def editConocimiento(cls, id, descripcion, categoria, explicacion):
        conocimiento = cls.by_id_instance(id)
        conocimiento.descripcion  = descripcion
        conocimiento.categoria  = categoria
        conocimiento.explicacion  = explicacion
        conocimiento.put()

    @classmethod
    def deleteConocimiento(cls,id):
        conocimiento = cls.by_id_instance(id) 
        conocimiento.isDeleted = True
        conocimiento.put()
    
    @classmethod
    def registrar(cls, descripcion, categoria, explicacion):
        return Conocimiento(parent = conocimientos_key(),
                    descripcion  = descripcion,
                    categoria  = categoria,
                    explicacion  = explicacion,
                    isDeleted = False)
