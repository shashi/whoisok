#!/usr/bin/env python
#
# main.py
#

import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from appengine_utilities import *

# OAuth
import twitter_oauth
import facebook_oauth

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(
      'templates/home.html', {}))

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/auth_twitter', twitter_oauth.LoginHandler),
  ('/auth_facebook', facebook_oauth.LoginHandler)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
