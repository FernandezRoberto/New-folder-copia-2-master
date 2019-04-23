import os
import sys
import webapp2

from requests_toolbelt.adapters import appengine
from google.appengine.ext import vendor
# Add any libraries installed in the "lib" folder.
vendor.add('lib')

appengine.monkeypatch()

sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

from controllers import *
from models import *
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

LETRAS_NUMEROS_REGEX    = r'((?:[0-9a-zA-Z]+?)*)'
DIGITOS_REGEX    = r'((?:[0-9]+?)*)'

application = webapp2.WSGIApplication([('/', Index),
    ('/categoria/crearCategoria', CrearCategoria),
    ('/categoria/listarCategoria', ListarCategoria),
    ('/categoria/editar/' + DIGITOS_REGEX, EditarCategoria),
    ('/categoria/borrar/' + DIGITOS_REGEX, EliminarCategoria),
    ('/medicamento/crearMedicamento', CrearMedicamento),
    ('/medicamento/listarMedicamento', ListarMedicamento),
    ('/medicamento/editarMedicamento/' + DIGITOS_REGEX, EditarMedicamento),
    ('/medicamento/borrarMedicamento/' + DIGITOS_REGEX, EliminarMedicamento),
    ('/conocimientos/crearConocimiento', CrearConocimiento),
    ('/conocimientos/listarConocimiento', ListarConocimiento),
    ('/conocimiento/editar/' + DIGITOS_REGEX, EditarConocimiento),
    ('/conocimiento/borrar/' + DIGITOS_REGEX, EliminarConocimiento),
    ('/paciente/crearPaciente', CrearPaciente),
    ('/paciente/mostrarPacientes', MostrarPacientes),
    ('/paciente/editar/' + DIGITOS_REGEX, EditarPaciente),
    ('/paciente/cita/' + DIGITOS_REGEX, CitaPaciente),
    ('/paciente/reconsulta/' + DIGITOS_REGEX, ReconsultaPaciente),
    ('/paciente/eliminar/' + DIGITOS_REGEX, EliminarPaciente),
    ('/historia_clinica/crear', CrearHistoriaClinica),
    ('/historia_clinica/listarDiaActual', ListarHistoriaClinicaDiaActual),
    ('/historia_clinica/listar', ListarHistoriaClinica),
    ('/historia_clinica/ver/' + DIGITOS_REGEX, VerHistoriaClinica),
    ('/historia_clinica/editar/' + DIGITOS_REGEX, EditarHistoriaClinica),
    ('/inferencia/listar', RealizarPrediccion),
    ('/inferencia/predecir', RealizarPrediccion),
    ('/inferencia/reentrenar', Reentrenar),
    ('/contact', Contact),
    ('/user/login', UserLogin),
    ('/user/logout', UserLogout),
    ('/user/register', CreateUser),
    ('/user/show', ShowUsers),
    ('/user/edit/' + DIGITOS_REGEX, EditUser),
    ('/user/delete/' + DIGITOS_REGEX, DeleteUser),
    ('/.*', NotFound)], debug=True)
