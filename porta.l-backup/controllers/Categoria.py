from Base import BaseHandler

import jinja2
import os
import logging
import webapp2
import json

from models.Categoria import Categoria

class CrearCategoria(BaseHandler):
    def get(self):
        self.init()
        self.params['Current'] = 'Categoria'
        self.render('categorias/crearCategoria.html', **self.params)

    def post(self):
        n = Categoria.registrar(self.request.get('nombre')) 
        n.put()
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
          'url': '/categoria/crearCategoria', 
          'message': 'Categoria registrado con exito',
        } 
        self.response.out.write(json.dumps(obj))

class ListarCategoria(BaseHandler):
    def get(self):
        self.init()
        categorias = Categoria.get_all();
        self.params['categorias'] = categorias
        self.render('categorias/listarCategoria.html', **self.params)

class EditarCategoria(BaseHandler):
    def post(self, note_id):
        iden = int(note_id)
        Categoria.editarCategoria(iden,
          self.request.get('nombre'))
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
          'url': '/categoria/listarCategoria', 
          'message':'Categoria actualizado exitosamente',
        } 
        self.response.out.write(json.dumps(obj))

    def get(self, note_id):
        self.init()
        iden = int(note_id)
        categoria = Categoria.by_id(iden)
        self.render_template('/categorias/editarCategoria.html', {'categoria': categoria},)

class EliminarCategoria(BaseHandler):
    def get(self, note_id):
        self.init()
        iden = int(note_id)
        Categoria.deleteCategoria(iden)
        return webapp2.redirect('/categoria/crearCategoria')