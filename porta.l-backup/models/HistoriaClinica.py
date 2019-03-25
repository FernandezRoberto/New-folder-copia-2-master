from google.appengine.ext import db
import logging

def historia_key(group = 'default'):
    return db.Key.from_path('historia', group)

class DictModel(db.Model):
    def to_dict(self):
       resp =  dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       resp['id'] = self.key().id()
       return resp

class HistoriaClinica(DictModel):
    fecha_apertura = db.DateProperty()
    paciente_id = db.IntegerProperty(64)
    observaciones = db.TextProperty()
    afroamericano = db.BooleanProperty()
    antecedentes_miopia = db.BooleanProperty()
    diabetes = db.BooleanProperty()

    @classmethod
    def get_all(cls):
        result = db.GqlQuery('SELECT * FROM HistoriaClinica')
        response = []

        for res in result:
            response.append(res.to_dict())

        return response

    @classmethod
    def by_id(cls, historia_clinica_id):
        historia_clinica = HistoriaClinica.get_by_id(historia_clinica_id)

        if historia_clinica:
            return historia_clinica
        else:
            return None

    def save_historia_clinica(self):
        self.put()

    def update_historia_clinica(self):
        self.put()

    def to_dict(self):
        resp = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        resp['id'] = self.key().id()
        return resp
