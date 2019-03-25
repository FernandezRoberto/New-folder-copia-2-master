from Base import BaseHandler
from models.Paciente import Paciente

import jinja2
import os
import logging
import webapp2
import json

class CrearPaciente(BaseHandler):
    def get(self):
        self.init()
        self.params['Current'] = 'Paciente'
        self.render('pacientes/crearPaciente.html', **self.params)

    def post(self):
        n = Paciente.register(
            self.request.get('paterno'),
            self.request.get('materno'),
            self.request.get('nombre'),
            self.request.get('fechaNacimiento'),
            self.request.get('direccion'),
            self.request.get('tipoDocumento'),
            self.request.get('nroDocumento'),
            self.request.get('estadoCivil'),
            self.request.get('ocupacion'),
            self.request.get('fechaCita')
        ) 
        n.put()
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
          'url': '/paciente/mostrarPacientes', 
          'message':'Paciente registrado con exito',
        } 
        self.response.out.write(json.dumps(obj))    

class MostrarPacientes(BaseHandler):
    def get(self):
        self.init()
        pacientes = Paciente.get_all()
        self.params['pacientes'] = pacientes
        self.render('pacientes/listarPacientes.html', **self.params)

class ReconsultaPaciente(BaseHandler):
    def post(self, note_id):
        iden = int(note_id)
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        user = dict(
          iden = iden,
          nombre = user_json.get("nombre", "").strip(),
          paterno = user_json.get("paterno", "").strip(),
          fechaCita = user_json.get("fechaCita", "").strip(),
          fechaReconsulta = user_json.get("fechaReconsulta","").strip()
        )
        Paciente.editPacienteReconsulta(user['iden'], user['fechaCita'], user['fechaReconsulta'])
        self.response.headers['Content-Type'] = 'application/json'   
        response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
        self.response.out.write(json.dumps(response))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        paciente = Paciente.by_id(iden)
        self.params['paciente'] = paciente
        self.render('/pacientes/reconsulta.html', **self.params)
        #self.render_template('/pacientes/reconsulta.html', { 'paciente': paciente })

class EditarPaciente(BaseHandler):
    def post(self, note_id):
        iden = int(note_id)
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        user = dict(
          iden = iden,
          paterno = user_json.get("paterno", "").strip(),
          materno = user_json.get("materno", "").strip(),
          nombre = user_json.get("nombre", "").strip(),
          fechaNacimiento = user_json.get("fechaNacimiento", "").strip(),
          direccion = user_json.get("direccion", "").strip(),
          tipoDocumento = user_json.get("tipoDocumento", "").strip(),
          nroDocumento = user_json.get("nroDocumento", "").strip(),
          estadoCivil = user_json.get("estadoCivil", "").strip(),
          ocupacion = user_json.get("ocupacion", "").strip(),
          fechaCita = user_json.get("fechaCita", "").strip(),
          fechaReconsulta = user_json.get("fechaReconsulta","").strip()
        )
        Paciente.editPaciente(user['iden'], user['paterno'], user['materno'], user['nombre'], user['fechaNacimiento'], user['direccion'], user['tipoDocumento'], user['nroDocumento'], user['estadoCivil'], user['ocupacion'], user['fechaCita'], user['fechaReconsulta'])
        self.response.headers['Content-Type'] = 'application/json'   
        response = { 'message': user['nombre']+' ' + user['paterno'] + ' modificado con exito', 'redirect_url': '/paciente/mostrarPacientes' }
        self.response.out.write(json.dumps(response))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        paciente = Paciente.by_id(iden)
        self.params['paciente'] = paciente
        self.render('/pacientes/editarPaciente.html', **self.params)

class EliminarPaciente(BaseHandler):

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        Paciente.deletePaciente(iden)
        return webapp2.redirect('/paciente/mostrarPacientes')
