from google.appengine.ext import db
from google.appengine.ext.blobstore import blobstore
import logging

def categorias_key(group = 'default'):
    return db.Key.from_path('categorias', group)

class DictModel(db.Model):
    def to_dict(self):
       resp =  dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       resp['id'] = self.key().id()
       return resp

class Categoria(DictModel):
    nombre = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    isDeleted = db.BooleanProperty(required = True, default = False)

    @classmethod
    def by_id(cls, uid):
        categoria = Categoria.get_by_id(uid, parent = categorias_key())
        if categoria:
            return categoria.to_dict()
        else:
            return None

    @classmethod
    def by_id_instance(cls, uid):
        categoria = Categoria.get_by_id(uid, parent = categorias_key())
        if categoria:
            return categoria
        else:
            return None

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM Categoria where isDeleted = False")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def editarCategoria(cls, id, nombre):
        categoria = cls.by_id_instance(id)
        categoria.nombre = nombre
        categoria.put()

    @classmethod
    def registrar(cls, nombre):
        return Categoria(parent = categorias_key(),
                    nombre  = nombre,
                    deleted = False)

    @classmethod
    def deleteCategoria(cls,id):
        categoria = cls.by_id_instance(id) 
        categoria.isDeleted = True
        categoria.put()