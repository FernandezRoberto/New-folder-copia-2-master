
import datetime
import json
import requests
import webapp2

from Base import BaseHandler
import jinja2
import os
import logging
import webapp2
import json

from models import Paciente

inference_url = 'http://localhost:5000/inference'
model_graph_url = 'http://localhost:5000/model/graph'


class Reentrenar(BaseHandler):
    def post(self):
        result = requests.post(inference_url + '/retrain')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(result.text)


class RealizarPrediccion(BaseHandler):
    def get(self):
        self.init()

        errores_response = json.loads(requests.get(inference_url + '/list_misclassified').text)
        errores = []

        lista_sintomas = {
            'dolor_ocular_severo': 'Dolor ocular severo',
            'enrojecimiento_ojo': 'Enrojecimiento del ojo',
            'nauseas_vomitos':  'Nauseas / vomitos',
            'vision_borrosa': 'Vision borrosa',
            'halos': 'Halos alrededor de la luz',
            'perdida_vision_periferica': 'Perdida de la vision periferica',
            'vision_tunel': 'Vision de tunel',
            'presion_intraocular': 'Presion intraocular'
        }

        for err in errores_response:
            sintomas = 'Presion intraocular: ' + err['presion_intraocular'] + '<br /><ul>'

            for llave in err:
                if err[llave] == 'True' and llave in lista_sintomas:
                    sintomas += '<li>' + lista_sintomas[llave] + '</li>'

            sintomas += '</ul>'

            detalle = {
                'fecha': err['fecha'],
                'sintomas': sintomas,
                'probabilidad_glaucoma': str(float(err['probabilidad_glaucoma']) * 100) + '%',
                'observaciones': err['observaciones'],
                'diagnostico': err['diagnostico'],
                'receta': err['receta']
            }

            errores.append(detalle)

        self.render_template('inferencia/listarErrores.html',
                             {'errores': errores, 'model_graph_url': model_graph_url})

    def post(self):
        historia_clinica = json.loads(self.request.body)
        paciente = Paciente.by_id(long(historia_clinica['paciente_id']))
        today = datetime.date.today()

        fecha_nacimiento = datetime.datetime.strptime(paciente['fechaNacimiento'], '%Y-%m-%d')

        edad = today.year - fecha_nacimiento.year - \
            ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        grupo_edad = None

        if 0 <= edad <= 35:
            grupo_edad = '0'
        elif 36 <= edad <= 60:
            grupo_edad = '1'
        elif edad > 60:
            grupo_edad = '2'

        criteria = {
            'dolor_ocular_severo': '1' if historia_clinica['dolor_ocular_severo'] else '0',
            'enrojecimiento_ojo': '1' if historia_clinica['enrojecimiento_ojo'] else '0',
            'nauseas_vomitos': '1' if historia_clinica['nauseas_vomitos'] else '0',
            'vision_borrosa': '1' if historia_clinica['vision_borrosa'] else '0',
            'halos': '1' if historia_clinica['halos'] else '0',
            'perdida_vision_periferica': '1' if historia_clinica['perdida_vision_periferica'] else '0',
            'vision_tunel': '1' if historia_clinica['vision_tunel'] else '0',
            'grupo_edad': grupo_edad,
            'afroamericano': '1' if historia_clinica['afroamericano'] else '0',
            'grado_miopia': historia_clinica['grado_miopia'],
            'antecedentes_miopia': '1' if historia_clinica['antecedentes_miopia'] else '0',
            'presion_intraocular_mayor_22': '1' if float(historia_clinica['presion_intraocular']) > 22 else '0',
            'usa_esteroides': '1' if historia_clinica['usa_esteroides'] else '0',
            'diabetes': '1' if historia_clinica['diabetes'] else '0',
        }

        result = requests.post(inference_url + '/predict', json=criteria)

        self.response.headers['Content-Type'] = 'application/json'

        res_json = json.loads(result.text)

        res = {
            'prediction': res_json['prediction'],
            'probability': res_json['probability'][0]['1']
        }

        self.response.out.write(json.dumps(res))
