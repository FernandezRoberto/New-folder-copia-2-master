from Base import BaseHandler
from models.Paciente import Paciente

import jinja2
import os
import logging
import webapp2
import json
import datetime

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
        pacientesValido = Paciente.get_nroDocumento(user['nroDocumento'])
        if (len(pacientesValido) == 0 ):
          n.put()
          self.response.headers['Content-Type'] = 'application/json'   
          obj = {
            'url': '/paciente/mostrarPacientes', 
            'message':'Paciente registrado con exito',
          } 
          self.response.out.write(json.dumps(obj))
        else:    
          self.response.headers['Content-Type'] = 'application/json'   
          response = { 'message': 'El Usuario con '+user['tipoDocumento']+':'+user['nroDocumento']+' ya existe, ingrese otro usuario', 'redirect_url': '/paciente/registrarPacientes'}
          self.response.out.write(json.dumps(response))

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
        pacientesConCita = Paciente.get_fechaCita(user['fechaReconsulta'])
        pacientesConReconsulta = Paciente.get_fechaReconsulta(user['fechaReconsulta'])
        ahora = datetime.datetime.now()
        month = ahora.month
        year = "%s%s" % ('', ahora.year)
        day = "%s%s" % ('', ahora.day)
        if(ahora.month<9):
            month = "%s%s" % ('0', ahora.month)
        if(ahora.day<9):
          day = "%s%s" % ('0', ahora.day)
        print(day);
        print(user['fechaReconsulta'][8:10])
        print(user['fechaReconsulta'][00:04] >= year)
        if user['fechaReconsulta'][00:04] >= year:
          if user['fechaReconsulta'][00:04] == year :
            if user['fechaReconsulta'][05:07] >= month:
              if user['fechaReconsulta'][00:04] == year:
                if user['fechaReconsulta'][8:10] >= day:
                  if user['fechaReconsulta'][11:13] >= '08' and user['fechaReconsulta'][11:13] <= '18' :
                    if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                      Paciente.editPacienteReconsulta(user['iden'], user['fechaReconsulta'])
                      self.response.headers['Content-Type'] = 'application/json'   
                      response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                      self.response.out.write(json.dumps(response))
                    else:
                      self.response.headers['Content-Type'] = 'application/json'   
                      response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                      self.response.out.write(json.dumps(response))
                  else:
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                    self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'El dia de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
              else:
                if user['fechaReconsulta'][11:13] >= '08' and user['fechaReconsulta'][11:13] <= '18' :
                  if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                    Paciente.editPacienteReconsulta(user['iden'], user['fechaReconsulta'])
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                    self.response.out.write(json.dumps(response))
                  else:
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                    self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
            else:
              self.response.headers['Content-Type'] = 'application/json'   
              response = { 'message': 'El mes de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
              self.response.out.write(json.dumps(response))
          else:
            if user['fechaReconsulta'][00:04] == year :
              if user['fechaReconsulta'][8:10] >= day:
                if user['fechaReconsulta'][11:13] >= '08' and user['fechaReconsulta'][11:13] <= '18' :
                  if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                    Paciente.editPacienteReconsulta(user['iden'], user['fechaReconsulta'])
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                    self.response.out.write(json.dumps(response))
                  else:
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                    self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
              else:
                self.response.headers['Content-Type'] = 'application/json'   
                response = { 'message': 'El dia de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
                self.response.out.write(json.dumps(response))
            else:
              if user['fechaReconsulta'][11:13] >= '08' and user['fechaReconsulta'][11:13] <= '18' :
                if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                  Paciente.editPacienteReconsulta(user['iden'], user['fechaReconsulta'])
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La reconsulta de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                  self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
              else:
                self.response.headers['Content-Type'] = 'application/json'   
                response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                self.response.out.write(json.dumps(response))
        else:
          self.response.headers['Content-Type'] = 'application/json'   
          response = { 'message': 'El anio de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
          self.response.out.write(json.dumps(response))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        paciente = Paciente.by_id(iden)
        self.params['paciente'] = paciente
        self.render('/pacientes/reconsulta.html', **self.params)
        #self.render_template('/pacientes/reconsulta.html', { 'paciente': paciente })

class CitaPaciente(BaseHandler):
    def post(self, note_id):
        iden = int(note_id)
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        user = dict(
          iden = iden,
          nombre = user_json.get("nombre", "").strip(),
          paterno = user_json.get("paterno", "").strip(),
          fechaCita = user_json.get("fechaCita", "").strip(),
          fechaReconsulta = user_json.get("fechaReconsulta", "").strip()
        )
        pacientesConCita = Paciente.get_fechaCita(user['fechaCita'])
        pacientesConReconsulta = Paciente.get_fechaReconsulta(user['fechaCita'])
        ahora = datetime.datetime.now()
        month = ahora.month
        year = "%s%s" % ('', ahora.year)
        day = "%s%s" % ('', ahora.day)
        if(ahora.month<9):
            month = "%s%s" % ('0', ahora.month)
        if(ahora.day<9):
          day = "%s%s" % ('0', ahora.day)
        print(day);
        print(user['fechaCita'][8:10])
        print(user['fechaCita'][8:10] >= day)
        if user['fechaCita'][00:04] >= year:
          if user['fechaCita'][00:04] == year :
            if user['fechaCita'][05:07] >= month:
              if user['fechaCita'][00:04] == year:
                if user['fechaCita'][8:10] >= day:
                  if user['fechaCita'][11:13] >= '08' and user['fechaCita'][11:13] <= '18' :
                    if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                      Paciente.editPacienteCita(user['iden'], user['fechaCita'])
                      self.response.headers['Content-Type'] = 'application/json'   
                      response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                      self.response.out.write(json.dumps(response))
                    else:
                      self.response.headers['Content-Type'] = 'application/json'   
                      response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                      self.response.out.write(json.dumps(response))
                  else:
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                    self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'El dia de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
              else:
                if user['fechaCita'][11:13] >= '08' and user['fechaCita'][11:13] <= '18' :
                  if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                    Paciente.editPacienteCita(user['iden'], user['fechaCita'])
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                    self.response.out.write(json.dumps(response))
                  else:
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                    self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
            else:
              self.response.headers['Content-Type'] = 'application/json'   
              response = { 'message': 'El mes de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
              self.response.out.write(json.dumps(response))
          else:
            if user['fechaCita'][00:04] == year :
              if user['fechaCita'][8:10] >= day:
                if user['fechaCita'][11:13] >= '08' and user['fechaCita'][11:13] <= '18' :
                  if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                    Paciente.editPacienteCita(user['iden'], user['fechaCita'])
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La cita de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                    self.response.out.write(json.dumps(response))
                  else:
                    self.response.headers['Content-Type'] = 'application/json'   
                    response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                    self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
              else:
                self.response.headers['Content-Type'] = 'application/json'   
                response = { 'message': 'El dia de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
                self.response.out.write(json.dumps(response))
            else:
              if user['fechaCita'][11:13] >= '08' and user['fechaCita'][11:13] <= '18' :
                if (len(pacientesConReconsulta) == 0 and len(pacientesConCita) == 0 ):
                  Paciente.editPacienteCita(user['iden'], user['fechaCita'])
                  self.response.headers['Content-Type'] = 'application/json'
                  response = { 'message': 'La reconsulta de ' + user['nombre']+' ' + user['paterno'] + ' fue registrada con exito', 'redirect_url': '/paciente/mostrarPacientes' }
                  self.response.out.write(json.dumps(response))
                else:
                  self.response.headers['Content-Type'] = 'application/json'   
                  response = { 'message': 'La fecha de la reconsulta ya esta tomada, seleccione otra fecha', 'redirect_url': '/paciente/mostrarPacientes'}
                  self.response.out.write(json.dumps(response))
              else:
                self.response.headers['Content-Type'] = 'application/json'   
                response = { 'message': 'La fecha de la reconsulta es invalida, por favor seleccione otra fecha (8:00am-6:00pm)', 'redirect_url': '/paciente/mostrarPacientes'}
                self.response.out.write(json.dumps(response))
        else:
          self.response.headers['Content-Type'] = 'application/json'   
          response = { 'message': 'El anio de la reconsulta es pasada , por favor seleccione otra fecha actual', 'redirect_url': '/paciente/mostrarPacientes'}
          self.response.out.write(json.dumps(response))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        paciente = Paciente.by_id(iden)
        self.params['paciente'] = paciente
        self.render('/pacientes/cita.html', **self.params)
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
