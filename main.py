#!/usr/bin/env python
#
# main.py
#

import cgi
import datetime
import wsgiref.handlers

# date time parser setup
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
c = pdc.Constants()
c.BirthdayEpoch = 80
dateparser = pdt.Calendar(c)
import time

# appengine modules
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
      'templates/home.html', {'msg' : self.request.get('msg')}))

class WhoIsOkHandler(webapp.RequestHandler):
  def get(self):
    epoch = self.request.get('epoch')
    data = {}
    try:
      dateparser.parse(epoch)
      data['interpretation'] = time.strftime('%A, %d %B %Y %I:%M%p GMT %z')
    except:
      self.redirect('/?msg=Invalid%20time!')
    #ok = twitter_oauth.who_since(epoch, self)

    #data['people_ok'] = ok
    self.response.out.write(template.render('templates/whoisok.html', data))
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
