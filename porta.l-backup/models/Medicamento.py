from google.appengine.ext import db
from google.appengine.ext.blobstore import blobstore
import logging

def medicamentos_key(group = 'default'):
    return db.Key.from_path('medicamentos', group)

class DictModel(db.Model):
    def to_dict(self):
       resp =  dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       resp['id'] = self.key().id()
       return resp

class Medicamento(DictModel):
    nombre = db.StringProperty(required = True)
    concentracion = db.StringProperty(required = True)
    docis = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    isDeleted = db.BooleanProperty(required = True, default = False)

    @classmethod
    def by_id(cls, uid):
        medicamento = Medicamento.get_by_id(uid, parent = medicamentos_key())
        if medicamento:
            return medicamento.to_dict()
        else:
            return None

    @classmethod
    def by_id_instance(cls, uid):
        medicamento = Medicamento.get_by_id(uid, parent = medicamentos_key())
        if medicamento:
            return medicamento
        else:
            return None

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM Medicamento where isDeleted = False")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def editarMedicamento(cls, id, nombre, concentracion, docis):
        medicamento = cls.by_id_instance(id)
        medicamento.nombre = nombre
        medicamento.concentracion = concentracion
        medicamento.docis = docis
        medicamento.put()

    @classmethod
    def registrar(cls, nombre, concentracion , docis):
        return Medicamento(parent = medicamentos_key(),
                    nombre  = nombre,
                    concentracion  = concentracion,
                    docis  = docis,
                    deleted = False)

    @classmethod
    def deleteMedicamento(cls,id):
        medicamento = cls.by_id_instance(id) 
        medicamento.isDeleted = True
        medicamento.put()