#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gdata.spreadsheet.text_db

class MakeHTML:

    def post(self):
      client = gdata.spreadsheet.text_db.DatabaseClient('englishplactice.appspot.com@gmail.com', 'ecitcalp')
      db = client.GetDatabases(name=u'DUO')[0]
      return MakeHTML.make_html(db.GetTables(name=u'root')[0]).encode("utf-8")

    @classmethod
    def html_escape(cls,text):
      MakeHTML.html_escape_table = {
        #  u"&": u"&amp;",
        u'"': u"&quot;",
        u"'": u"&apos;",
        u">": u"&gt;",
        u"<": u"&lt;",
      }
      return u"".join(MakeHTML.html_escape_table.get(c,c) for c in text)

    @classmethod
    def make_html(cls,table):
      html = u""
      scripts = []
      current_prefecture = u"";
      for record in table.GetRecords(1, 999999999):
        html += record.content[u"通し番号"]
        html += ",";
        html += record.content[u"日本語"]
        html += ",";
        html += record.content[u"英語"]
        html += "\n";
      return html

def main():
    make_html = MakeHTML()
    print make_html.post()


if __name__ == '__main__':
    main()

