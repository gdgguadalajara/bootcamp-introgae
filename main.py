#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Introducción a Google App Engine
    GDG Guadalajara, 2014

    @jn6h - Nazareth Gutiérrez
                                      """
import webapp2
import cgi


MAIN_PAGE_HTML = """
<!doctype html>
<html>
  <body>
    <form action="/save" method="post">
      <div>
        <label>
          Nombre del producto:
          <input type="text" name="product_name">
        </label>
      </div>
      <div>
        <input type="submit" value="Guardar">
      </div>
    </form>
  </body>
</html>
"""


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'

    self.response.write(MAIN_PAGE_HTML)


class ProductHandler(webapp2.RequestHandler):

  def post(self):
    product_name = self.request.get('product_name')

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Has ingresado %s' % cgi.escape(product_name))


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/save', ProductHandler)
], debug=True)
