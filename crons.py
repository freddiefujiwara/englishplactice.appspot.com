#!/usr/bin/env python
# coding: utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from django.utils import simplejson
import urllib
import re
import gdata.spreadsheet.text_db

class Text(db.Model):
  text_id = db.IntegerProperty()
  japanese = db.TextProperty()
  english = db.TextProperty()

class CrawlSpread:

    def crawl(self):
      client = gdata.spreadsheet.text_db.DatabaseClient('englishplactice.appspot.com@gmail.com', 'ecitcalp')
      db = client.GetDatabases(name=u'DUO')[0]
      table = db.GetTables(name=u'root')[0]
      for record in table.GetRecords(1, 999999999):
      	text = Text.gql('WHERE text_id = :1',int(record.content[u"通し番号"])).get()
        record.content[u"英語"] = re.compile('"').sub("",record.content[u"英語"])
      	if text is None:
          text = Text(text_id=int(record.content[u"通し番号"]),japanese=record.content[u"日本語"],english=record.content[u"英語"])
      	else:
          text.japanese=record.content[u"日本語"]
          text.english =record.content[u"英語"]
      	text.put()

class CrawlSpreadHandler(webapp.RequestHandler):
    
    def __init__(self):
        self.application = CrawlSpread()
    
    def get(self):
        self.application.crawl()

def main():
    application = webapp.WSGIApplication([('/crons/crawl_spread', CrawlSpreadHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
