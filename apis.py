import os
import re
import urllib
import urllib2
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson

class Text(db.Model):
  text_id = db.IntegerProperty()
  japanese = db.TextProperty()
  english = db.TextProperty()

class TTSAPI(webapp.RequestHandler):
  def get(self):
    params = urllib.urlencode({'ie':'UTF-8', 'tl':'en','q':self.request.get('q')})
    headers = { 'User-Agent' : "Mozilla/4.0" }
    f = urllib2.urlopen(urllib2.Request('http://translate.google.com/translate_tts',params, headers))
    self.response.headers['Content-Type'] = 'audio/mpeg'
    self.response.out.write(f.read())

class TextAPI(webapp.RequestHandler):
  def get(self):
    jsons = []
    for text in Text.all():
      json = u""
      json += "{'id':"
      json += simplejson.dumps(text.text_id)
      json += ",'english':"
      json += simplejson.dumps(text.english)
      json += ",'japanese':"
      json += simplejson.dumps(text.japanese)
      json += "}"
      jsons.append(json)
    self.response.headers['Content-Type'] = 'text/x-json'
    callback = self.request.get('callback');
    if callback :
      p = re.compile('[^a-zA-Z0-9._]')
      callback = p.sub('',callback)
      self.response.out.write(callback + "(["+",".join(jsons)+"]);")
    else :
      self.response.out.write("["+",\n".join(jsons)+"]")

application = webapp.WSGIApplication(
                                     [('/apis/texts.js', TextAPI),('/apis/tts.mp3', TTSAPI)
                                     ],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
