#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Introducción a Google App Engine
    GDG Guadalajara, 2014

    @jn6h - Nazareth Gutiérrez
                                      """
import webapp2

class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello App Engine!')


application = webapp2.WSGIApplication([
  ('/', MainPage)
], debug=True)
