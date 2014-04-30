#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Introducción a Google App Engine
    GDG Guadalajara, 2014

    @jn6h - Nazareth Gutiérrez
                                      """
import webapp2
import cgi
import urllib

from google.appengine.ext import ndb

HEADER_PAGE_HTML = """
<!doctype html>
<html>
  <body>
"""

FORM_HTML = """
    <form action="/new" method="post">
      <div>
        <label>
          Notebook:
          <input type="text" name="stock_name" value="%s">
        </label>
      </div>
      <div>
        <label>
          TODO:
          <input type="text" name="todo">
        </label>
      </div>
      <div>
        <input type="submit" value="Agregar">
      </div>
    </form>
"""

FOOTER_PAGE_HTML = """
  </body>
</html>
"""

DEFAULT_STOCK_NAME = 'default_notebook'

def notebook_key(stock_name=DEFAULT_STOCK_NAME):
  return ndb.Key('Notebook', stock_name)


class Todo(ndb.Model):
  description = ndb.StringProperty(indexed=True)
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    self.response.write(HEADER_PAGE_HTML)

    stock_name = self.request.get('stock_name', DEFAULT_STOCK_NAME)
    ancestor_key = notebook_key(stock_name)

    todo_query = Todo.query(ancestor=ancestor_key).order(-Todo.date)
    todos = todo_query.fetch(20)

    self.response.write(FORM_HTML % stock_name)

    self.response.write('<ul>')
    for todo in todos:
      self.response.write('<li>%s</li>' % cgi.escape(todo.description))
    self.response.write('</ul>')

    self.response.write(FOOTER_PAGE_HTML)


class NewTodoHandler(webapp2.RequestHandler):

  def post(self):
    stock_name = self.request.get('stock_name', DEFAULT_STOCK_NAME)

    newTodo = Todo(parent=notebook_key(stock_name))
    newTodo.description = self.request.get('todo')
    newTodo.put()

    self.redirect('/?' + urllib.urlencode({'stock_name': stock_name}))


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/new', NewTodoHandler)
], debug=True)
