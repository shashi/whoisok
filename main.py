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

class WhoIsOkHandler(webapp.RequestHandler):
  def get(self):
    pass

application = webapp.WSGIApplication([
  ('/', MainPage),
  (r'/oauth/(.*)/(.*)', twitter_oauth.OAuthHandler),
  ('/oauth/facebook', facebook_oauth.LoginHandler),
  ('/whoisok', WhoIsOkHandler)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
