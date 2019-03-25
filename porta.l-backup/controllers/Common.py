import logging
from Base import BaseHandler

class Index(BaseHandler):
	def get(self):
		self.init()
		self.render('index.html', **self.params)

class Contact(BaseHandler):
	def get(self):
		self.init()
		self.params['Current'] = 'Contact'
		self.render('common/contact.html', **self.params)

class NotFound(BaseHandler):
	def get(self):
		self.error(404)
		self.render('common/404.html', **self.params)