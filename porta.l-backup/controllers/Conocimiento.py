from Base import BaseHandler

import jinja2
import os
import logging
import webapp2
import json

from models.Conocimiento import Conocimiento

class CrearConocimiento(BaseHandler):
    def get(self):
		self.init()
		self.params['Current'] = 'CrearConocimiento'
		self.render('conocimientos/crearConocimiento.html', **self.params)

    def post(self):
        n = Conocimiento.registrar(self.request.get('descripcion'), self.request.get('categoria'), self.request.get('explicacion')) 
        n.put()
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
          'url': '/conocimientos/listarConocimiento', 
          'message': self.request.get('categoria')+' registrado con exito',
        } 
        self.response.out.write(json.dumps(obj))  

class ListarConocimiento(BaseHandler):
    def get(self):
        self.init()
        conocimientos = Conocimiento.get_all();
        print "conocimientos: ",conocimientos[0]['id']
        self.params['conocimientos'] = conocimientos
        self.render('conocimientos/listarConocimiento.html', **self.params)

class EditarConocimiento(BaseHandler):
    def post(self, note_id):
        iden = int(note_id)
        Conocimiento.editConocimiento(iden,
         self.request.get('descripcion'),
          self.request.get('categoria'),
          self.request.get('explicacion'))
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
          'url': '/conocimientos/listarConocimiento', 
          'message': self.request.get('categoria')+' actualizado exitosamente',
        } 
        self.response.out.write(json.dumps(obj))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        conocimiento = Conocimiento.by_id(iden)
        self.render_template('/conocimientos/editarConocimiento.html', {'conocimiento': conocimiento},)

class EliminarConocimiento(BaseHandler):
    def get(self, note_id):
        self.init()
        iden = int(note_id)
        Conocimiento.deleteConocimiento(iden)
        return webapp2.redirect('/conocimientos/crearConocimiento')