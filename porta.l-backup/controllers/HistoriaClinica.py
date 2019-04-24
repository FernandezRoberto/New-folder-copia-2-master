from Base import BaseHandler

from datetime import date
import datetime
import json
import requests
import jinja2
import os
import logging
import webapp2


from google.appengine.ext import db
from Inferencia import inference_url

from models import Paciente
from models.Medicamento import Medicamento
from models.HistoriaClinica import HistoriaClinica
from models.Consulta import Consulta

def obtener_historia_clinica_completa(historia_clinica_id):
    historia_clinica = HistoriaClinica.by_id(long(historia_clinica_id))
    historia_clinica_id = historia_clinica.key().id()
    historia_clinica = historia_clinica.to_dict()
    paciente = Paciente.by_id(long(historia_clinica['paciente_id']))
    historia_clinica['paciente_apellido_paterno'] = paciente['paterno']
    historia_clinica['paciente_apellido_materno'] = paciente['materno']
    historia_clinica['paciente_nombre'] = paciente['nombre']
    historia_clinica['paciente_fecha_nacimiento'] = paciente['fechaNacimiento']
    historia_clinica['paciente_direccion'] = paciente['direccion']
    historia_clinica['paciente_ci'] = paciente['nroDocumento']
    historia_clinica['paciente_tipo_documento'] = paciente['tipoDocumento']
    historia_clinica['paciente_estado_civil'] = paciente['estadoCivil']
    historia_clinica['paciente_ocupacion'] = paciente['ocupacion']
    historia_clinica['paciente_fecha_reconsulta'] = paciente['fechaReconsulta']
    historia_clinica['paciente_fecha_cita'] = paciente['fechaCita']
    historia_clinica['paciente_is_deleted'] = paciente['isDeleted']

    historia_clinica['consultas'] = Consulta.get_all_by_historia_clinica_id(long(historia_clinica_id))

    return historia_clinica


class ListarHistoriaClinica(BaseHandler):
    def get(self):
        self.init()
        respuesta = []
        historias_clinicas = HistoriaClinica.get_all()
        print "hisssssssssssssssssssssssss: ", historias_clinicas
        for historia_clinica in historias_clinicas:
            paciente = Paciente.by_id(long(historia_clinica['paciente_id']))
            print "paciente: ", paciente
            respuesta.append({
                'id': historia_clinica['id'],
                'paciente_apellido_paterno': paciente['paterno'],
                'paciente_apellido_materno': paciente['materno'],
                'paciente_nombre': paciente['nombre'],
                'paciente_fecha_nacimiento': paciente['fechaNacimiento'],
                'paciente_fecha_reconsulta': paciente['fechaReconsulta'],
                'paciente_fecha_cita': paciente['fechaCita'],
                'paciente_is_deleted': paciente['isDeleted']
            })
        self.params['historias_clinicas'] = respuesta
        #self.render_template('historiasClinicas/listarHistoriasClinicas.html',
        #                     {'historias_clinicas': respuesta})
        self.render('historiasClinicas/listarHistoriasClinicas.html', **self.params)

class ListarHistoriaClinicaDiaActual(BaseHandler):
    def get(self):
        self.init()
        respuesta = []
        historias_clinicas = HistoriaClinica.get_all()

        for historia_clinica in historias_clinicas:
            paciente = Paciente.by_id(long(historia_clinica['paciente_id']))
            logging.warn(paciente['fechaCita'][0:10])
            if paciente['fechaCita'][0:10] == datetime.datetime.now().strftime("%Y-%m-%d") :
                respuesta.append({
                    'id': historia_clinica['id'],
                    'paciente_apellido_paterno': paciente['paterno'],
                    'paciente_apellido_materno': paciente['materno'],
                    'paciente_nombre': paciente['nombre'],
                    'paciente_fecha_nacimiento': paciente['fechaNacimiento'],
                    'paciente_fecha_reconsulta': paciente['fechaReconsulta'],
                    'paciente_fecha_cita': paciente['fechaCita'],
                    'paciente_is_deleted': paciente['isDeleted']
                })
        self.params['historias_clinicas'] = respuesta
        #self.render_template('historiasClinicas/listarHistoriasClinicas.html',
        #                     {'historias_clinicas': respuesta})
        self.render('historiasClinicas/listarHistoriasClinicasDiaActual.html', **self.params)

class CrearHistoriaClinica(BaseHandler):
    def get(self):
        self.init()
        self.params['post_url'] = '/historia_clinica/crear'
        self.render('historiasClinicas/crearHistoriaClinica.html',**self.params)

    @db.transactional(xg=True)
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        paciente = dict(
          paterno = user_json.get("paterno", "").strip(),
          materno = user_json.get("materno", "").strip(),
          nombre = user_json.get("nombre", "").strip(),
          fechaNacimiento = user_json.get("fechaNacimiento", "").strip(),
          direccion = user_json.get("direccion", "").strip(),
          tipoDocumento = user_json.get("tipoDocumento", "").strip(),
          nroDocumento = user_json.get("nroDocumento", "").strip(),
          estadoCivil = user_json.get("estadoCivil", "").strip(),
          ocupacion = user_json.get("ocupacion","").strip()
        )
        n = Paciente.register(paciente['paterno'], paciente['materno'], paciente['nombre'], paciente['fechaNacimiento'], paciente['direccion'], paciente['tipoDocumento'], paciente['nroDocumento'], paciente['estadoCivil'], paciente['ocupacion'])
        n.put()

        


        #historia_json = json.loads(self.request.body)

        #paciente = Paciente.register(historia_json['paterno'],
          #                historia_json['materno'],
          #                historia_json['nombre'],
           #               historia_json['fechaNacimiento'],
          #                historia_json['direccion'],
          #                historia_json['tipoDocumento'],
           #               historia_json['nroDocumento'],
           #               historia_json['estadoCivil'],
           #               historia_json['ocupacion'])

        #paciente.put()

        historia_clinica = HistoriaClinica()
        historia_clinica.fecha_apertura = datetime.date.today()
        historia_clinica.observaciones = user_json.get("observaciones","").strip() #historia_json['observaciones']

        historia_clinica.afroamericano = bool(user_json.get("afroamericano","").strip()) #bool(historia_json['afroamericano'])
        historia_clinica.antecedentes_miopia = bool(user_json.get("antecedentes_miopia","").strip()) #bool(historia_json['antecedentes_miopia'])
        historia_clinica.diabetes = bool(user_json.get("diabetes","").strip()) #bool(historia_json['diabetes'])
        historia_clinica.paciente_id = n.key().id()

        historia_clinica.save_historia_clinica()

        self.response.headers['Content-Type'] = 'application/json'   
      
        response = { 'message': user_json.get("nombre", "").strip() + ' fue registrado con exito', 'redirect_url': '/paciente/mostrarPacientes' }
        self.response.out.write(json.dumps(response))

        #self.response.write('{"response": "ok", "historia_clinica_id": "%s"}' % historia_clinica.key().id())


class VerHistoriaClinica(BaseHandler):
    def get(self, historia_clinica_id):
        self.init()
        historia_clinica = obtener_historia_clinica_completa(historia_clinica_id)
        consultas = historia_clinica['consultas']
        consultas_listado = []

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

        grados_miopia = {
            '0': 'Bajo',
            '1': 'Alto',
            '2': 'Muy Alto'
        }

        for consulta in consultas:
            sintomas = 'Presion intraocular: ' + consulta['presion_intraocular'] + '<br />' \
                       'Grado de miopia: ' + grados_miopia[consulta['grado_miopia']] + '<br /><ul>'

            for llave in consulta:
                if consulta[llave] == 'True' and llave in lista_sintomas:
                    sintomas += '<li>' + lista_sintomas[llave] + '</li>'

            sintomas += '</ul>'

            detalle = {
                'fecha': consulta['fecha'],
                'sintomas': sintomas,
                'probabilidad_glaucoma': str(float(consulta['probabilidad_glaucoma']) * 100) + '%',
                'observaciones': consulta['observaciones'],
                'diagnostico': consulta['diagnostico'],
                'receta': consulta['receta']
            }

            consultas_listado.append(detalle)
        
        historia_clinica['consultas'] = consultas_listado
        self.params['historia_clinica'] = historia_clinica
        self.render('historiasClinicas/verHistoriaClinica.html', **self.params)
        #self.render_template('historiasClinicas/verHistoriaClinica.html', {'historia_clinica': historia_clinica},**self.params)


class EditarHistoriaClinica(BaseHandler):
    def get(self, historia_clinica_id):
        self.init()
        medicamentos = Medicamento.get_all();
        
        historia_clinica = obtener_historia_clinica_completa(historia_clinica_id)
        ultima_consulta = Consulta.get_last_by_historia_clinica_id(historia_clinica_id)
        historia_clinica['ultima_consulta'] = ultima_consulta if ultima_consulta else {}
        self.params['historia_clinica'] = historia_clinica
        self.params['medicamentos'] = medicamentos
        self.render('historiasClinicas/editarHistoriaClinica.html', **self.params)
        #self.render_template('historiasClinicas/editarHistoriaClinica.html', {'historia_clinica': historia_clinica},**self.params)

    @db.transactional(xg=True)
    def put(self, historia_clinica_id):
        consulta = Consulta()
        historia_clinica = HistoriaClinica.by_id(long(historia_clinica_id))

        consulta_json = json.loads(self.request.body)

        historia_clinica.observaciones = consulta_json['observaciones_historia']
        historia_clinica.afroamericano = consulta_json['afroamericano']
        historia_clinica.diabetes = consulta_json['diabetes']
        historia_clinica.antecedentes_miopia = consulta_json['antecedentes_miopia']

        historia_clinica.put()

        consulta.historia_clinica_id = long(historia_clinica_id)
        consulta.fecha = datetime.datetime.now()
        consulta.dolor_ocular_severo = consulta_json['dolor_ocular_severo']
        consulta.enrojecimiento_ojo = consulta_json['enrojecimiento_ojo']
        consulta.nauseas_vomitos = consulta_json['nauseas_vomitos']
        consulta.vision_borrosa = consulta_json['vision_borrosa']
        consulta.halos = consulta_json['halos']
        consulta.perdida_vision_periferica = consulta_json['perdida_vision_periferica']
        consulta.vision_tunel = consulta_json['vision_tunel']
        consulta.grado_miopia = int(consulta_json['grado_miopia'])
        consulta.presion_intraocular = float(consulta_json['presion_intraocular'])
        consulta.usa_esteroides = consulta_json['usa_esteroides']
        consulta.observaciones = consulta_json['observaciones']
        consulta.diagnostico = consulta_json['diagnostico']
        consulta.receta = consulta_json['receta']
        consulta.tiene_glaucoma = consulta_json['tiene_glaucoma'] == '1'
        consulta.probabilidad_glaucoma = float(consulta_json['probabilidad_glaucoma'])
        consulta.prediccion_correcta = consulta_json['prediccion_correcta'] == 'yes'

        consulta.save()

        if consulta_json['prediccion_correcta'] == 'no':
            paciente = Paciente.by_id(historia_clinica.paciente_id)
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

            error = {
                'consulta': consulta.to_dict(),
                'criterios': {
                    'dolor_ocular_severo': '1' if consulta_json['dolor_ocular_severo'] else '0',
                    'enrojecimiento_ojo': '1' if consulta_json['enrojecimiento_ojo'] else '0',
                    'nauseas_vomitos': '1' if consulta_json['nauseas_vomitos'] else '0',
                    'vision_borrosa': '1' if consulta_json['vision_borrosa'] else '0',
                    'halos': '1' if consulta_json['halos'] else '0',
                    'perdida_vision_periferica': '1' if consulta_json['perdida_vision_periferica'] else '0',
                    'vision_tunel': '1' if consulta_json['vision_tunel'] else '0',
                    'grupo_edad': grupo_edad,
                    'afroamericano': '1' if consulta_json['afroamericano'] else '0',
                    'grado_miopia': consulta_json['grado_miopia'],
                    'antecedentes_miopia': '1' if consulta_json['antecedentes_miopia'] else '0',
                    'presion_intraocular_mayor_22': '1' if float(consulta_json['presion_intraocular']) > 22 else '0',
                    'usa_esteroides': '1' if consulta_json['usa_esteroides'] else '0',
                    'diabetes': '1' if consulta_json['diabetes'] else '0',
                }
            }

            requests.post(inference_url + '/report_misclassified', json=error)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('{"result": "ok"}')
