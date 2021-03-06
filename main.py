#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Introducción a Google App Engine
    GDG Guadalajara, 2014

    @jn6h - Nazareth Gutiérrez
                                      """
import os
import cgi
import urllib

import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
  autoescape=True,
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


DEFAULT_STOCK_NAME = 'default_notebook'

def notebook_key(stock_name=DEFAULT_STOCK_NAME):
  return ndb.Key('Notebook', stock_name)


class Todo(ndb.Model):
  description = ndb.StringProperty(indexed=True)
  author = ndb.UserProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'

    current_user = users.get_current_user()
    if not current_user:
      login_url = users.create_login_url(self.request.uri)
      self.redirect(login_url)
    else:
      logout_url = users.create_logout_url(self.request.uri)

      stock_name = self.request.get('stock_name', DEFAULT_STOCK_NAME)
      ancestor_key = notebook_key(stock_name)

      todo_query = Todo.query(ancestor=ancestor_key).order(-Todo.date)
      todos = todo_query.fetch(20)

      template_values = {
        'todos': todos,
        'stock_name': urllib.quote_plus(stock_name),
        'logout_url': logout_url,
        'current_user': current_user.nickname()
      }

      template = jinja_environment.get_template('todos.html')
      self.response.write(template.render(template_values))


class NewTodoHandler(webapp2.RequestHandler):

  def post(self):
    stock_name = self.request.get('stock_name', DEFAULT_STOCK_NAME)

    newTodo = Todo(parent=notebook_key(stock_name))

    if users.get_current_user():
      newTodo.author = users.get_current_user()

    newTodo.description = self.request.get('todo')
    newTodo.put()

    self.redirect('/?' + urllib.urlencode({'stock_name': stock_name}))


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/new', NewTodoHandler)
], debug=True)
