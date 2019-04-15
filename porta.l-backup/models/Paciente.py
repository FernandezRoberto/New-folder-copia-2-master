from google.appengine.ext import db
#from Encryption import Encript
from google.appengine.ext.blobstore import blobstore
import logging

def pacientes_key(group = 'default'):
    return db.Key.from_path('pacientes', group)


class DictModel(db.Model):
    def to_dict(self):
       resp =  dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       resp['id'] = self.key().id()
       return resp


class Paciente(DictModel):
    paterno = db.StringProperty(required = True)
    materno = db.StringProperty(required = True)
    nombre = db.StringProperty(required = True)
    fechaNacimiento = db.StringProperty(required = True)
    direccion = db.StringProperty(required = True)
    tipoDocumento = db.StringProperty(required = True,)
    nroDocumento = db.StringProperty(required = True)
    estadoCivil = db.StringProperty(required = True)
    ocupacion = db.StringProperty(required = True)
    fechaCita = db.StringProperty(required = False)
    fechaReconsulta = db.StringProperty(required = False)
    created = db.DateTimeProperty(auto_now_add = True)
    isDeleted = db.BooleanProperty(required = True, default = False)

    @classmethod
    def by_id(cls, uid):
        paciente = Paciente.get_by_id(uid, parent = pacientes_key())
        print "pacienteMod: ", paciente
        if paciente:
            return paciente.to_dict()
        else:
            return None

    @classmethod
    def by_id_instance(cls, uid):
        paciente = Paciente.get_by_id(uid, parent = pacientes_key())
        if paciente:
            return paciente
        else:
            return None

    @classmethod
    def get_all(cls):
        res = db.GqlQuery("SELECT * FROM Paciente where isDeleted = False")
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def get_fechaCita(cls, fechaCit):
        res = db.GqlQuery("SELECT * FROM Paciente where isDeleted = False AND fechaCita = :1",fechaCit)
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def get_fechaReconsulta(cls, fechaReconsul):
        res = db.GqlQuery("SELECT * FROM Paciente where isDeleted = False AND fechaReconsulta = :1",fechaReconsul)
        response = []
        for r in res:
            response.append(r.to_dict())
        return response

    @classmethod
    def by_nroDocumento(cls, nroDocumento):
        u = Paciente.all().filter('nroDocumento =', nroDocumento).get()
        return u

    @classmethod
    def editPaciente(cls, id, paterno, materno, nombre, fechaNacimiento, direccion, tipoDocumento, nroDocumento, estadoCivil, ocupacion, fechaCita, fechaReconsulta ):
        paciente = cls.by_id_instance(id)
        paciente.paterno = paterno
        paciente.materno = materno
        paciente.nombre = nombre
        paciente.fechaNacimiento = fechaNacimiento
        paciente.direccion = direccion
        paciente.tipoDocumento = tipoDocumento
        paciente.nroDocumento = nroDocumento
        paciente.estadoCivil = estadoCivil
        paciente.ocupacion = ocupacion
        paciente.fechaCita = fechaCita
        paciente.fechaReconsulta = fechaReconsulta
        paciente.put()

    @classmethod
    def editPacienteReconsulta(cls, id, fechaReconsulta):
        paciente = cls.by_id_instance(id)
        paciente.fechaReconsulta = fechaReconsulta
        paciente.put()

    @classmethod
    def editPacienteCita(cls, id, fechaCita):
        paciente = cls.by_id_instance(id)
        paciente.fechaCita = fechaCita
        paciente.put()

    @classmethod
    def deletePaciente(cls,id):
        paciente = cls.by_id_instance(id) 
        paciente.isDeleted = True
        paciente.put()

    @classmethod
    def register(cls, paterno, materno, nombre, fechaNacimiento, direccion, tipoDocumento, nroDocumento, estadoCivil, ocupacion):
        return Paciente(parent = pacientes_key(),
                    paterno = paterno, 
                    materno = materno,
                    nombre  = nombre, 
                    fechaNacimiento = fechaNacimiento, 
                    direccion = direccion,
                    tipoDocumento = tipoDocumento, 
                    nroDocumento = nroDocumento, 
                    estadoCivil = estadoCivil, 
                    ocupacion = ocupacion,
                    isDeleted = False)
