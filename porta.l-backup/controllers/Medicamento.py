from Base import BaseHandler

import jinja2
import os
import logging
import webapp2
import json

from models.Medicamento import Medicamento

class CrearMedicamento(BaseHandler):
    def get(self):
        self.init()
        self.params['Current'] = 'Medicamento'
        self.render('medicamentos/crearMedicamento.html', **self.params)

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        medicamento = dict(
          nombre = user_json.get("nombre", "").strip(),
          concentracion = user_json.get("concentracion", "").strip(),
          docis = user_json.get("docis", "").strip()
        )
        n = Medicamento.registrar(medicamento['nombre'], medicamento['concentracion'], medicamento['docis']) 
        n.put()
        self.response.headers['Content-Type'] = 'application/json'   
        response = { 'message':'Medicamento registrado con exito', 'redirect_url': '/medicamento/listarMedicamento' }
        self.response.out.write(json.dumps(response))

class ListarMedicamento(BaseHandler):
    def get(self):
        self.init()
        medicamentos = Medicamento.get_all();
        self.params['medicamentos'] = medicamentos
        self.render('medicamentos/listarMedicamento.html', **self.params)

class EditarMedicamento(BaseHandler):
    def post(self, note_id):
        iden = int(note_id)
        self.response.headers['Content-Type'] = 'application/json'
        user_json = json.loads(self.request.body)
        medicamento = dict(
          iden = iden,
          nombre = user_json.get("nombre", "").strip(),
          concentracion = user_json.get("concentracion", "").strip(),
          docis = user_json.get("docis", "").strip()
        )
        Medicamento.editarMedicamento(medicamento['iden'], medicamento['nombre'], medicamento['concentracion'], medicamento['docis']) 
        self.response.headers['Content-Type'] = 'application/json'   
        response = { 'message':'Medicamento modificado con exito', 'redirect_url': '/medicamento/listarMedicamento' }
        self.response.out.write(json.dumps(response))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        medicamento = Medicamento.by_id(iden)
        self.params['medicamento'] = medicamento
        self.render_template('/medicamentos/editarMedicamento.html', {'medicamento': medicamento},)

class EliminarMedicamento(BaseHandler):
    def get(self, note_id):
        self.init()
        iden = int(note_id)
        Medicamento.deleteMedicamento(iden)
        return webapp2.redirect('/medicamento/listarMedicamento')