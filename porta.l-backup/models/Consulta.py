from google.appengine.ext import db

import logging
class Consulta(db.Model):
    historia_clinica_id = db.IntegerProperty(64)
    fecha = db.DateTimeProperty()
    dolor_ocular_severo = db.BooleanProperty()
    enrojecimiento_ojo = db.BooleanProperty()
    nauseas_vomitos = db.BooleanProperty()
    vision_borrosa = db.BooleanProperty()
    halos = db.BooleanProperty()
    perdida_vision_periferica = db.BooleanProperty()
    vision_tunel = db.BooleanProperty()
    afroamericano = db.BooleanProperty()
    grado_miopia = db.IntegerProperty()
    antecedentes_miopia = db.BooleanProperty()
    presion_intraocular = db.FloatProperty()
    usa_esteroides = db.BooleanProperty()
    motivo = db.TextProperty()
    observaciones = db.TextProperty()
    diagnostico = db.TextProperty()
    receta = db.TextProperty()
    tiene_glaucoma = db.BooleanProperty()
    probabilidad_glaucoma = db.FloatProperty()
    prediccion_correcta = db.BooleanProperty()

    @classmethod
    def get_all_by_historia_clinica_id(cls, historia_clinica_id):
        consultas = db.GqlQuery('SELECT * FROM Consulta WHERE historia_clinica_id=%s ORDER BY fecha DESC' % historia_clinica_id)
        result = []

        for consulta in consultas:
            result.append(consulta.to_dict())

        return result

    @classmethod
    def get_last_by_historia_clinica_id(cls, historia_clinica_id):
        consultas = db.GqlQuery(
            'SELECT * FROM Consulta WHERE historia_clinica_id=%s ORDER BY fecha DESC LIMIT 1' % historia_clinica_id)

        result = []

        for consulta in consultas:
            result.append(consulta.to_dict())

        return result[0] if result else None

    @classmethod
    def by_id(cls, consulta_id):
        consulta = Consulta.get_by_id(consulta_id)

        if consulta:
            return consulta.to_dict()
        else:
            return None

    def to_dict(self):
        resp = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        resp['id'] = self.key().id()
        return resp
