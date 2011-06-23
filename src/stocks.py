'''
Created on 18/06/2011

@author: crispamares
'''
import urllib2, HTMLParser
import pprint

class StockParser(HTMLParser.HTMLParser):

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.inside_table = False
        self.inside_tr = False
        self.inside_td = False
        self.stocks = {}
    
        self.actual_data = []
        
        self.handle_actual_tag = self.handle_table
        self.i = 0

    def handle_starttag(self, tag, attrs):
        if tag == self.next_tag():
            self.handle_actual_tag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "table" and self.inside_table:
            self.inside_table = False
            self.inside_td = False
            self.inside_tr = False
            self.handle_actual_tag = lambda t,a: None
        if self.inside_tr and tag == "tr":
            self.stocks[self.actual_data[0].strip()] = map(lambda s: float(s.replace(".","").replace(",",".")), self.actual_data[1:-2]) + self.actual_data[-2:]
            self.actual_data = []
            
    def handle_data(self, data):
        if self.inside_tr and data != "\r\n":
            self.actual_data.append(data)
    
    def handle_table(self, tag, attrs):
        if dict(attrs).get('width') == '96%':
            self.inside_table = True
            self.handle_actual_tag = self.handle_tr
    
    def handle_tr(self, tag, attrs):
        self.i += 1
        if self.i > 1:
            self.inside_tr = True
#            self.handle_actual_tag = self.handle_td
#    
#    def handle_td(self, tag, attrs):
#        pass
    
    def next_tag(self):
        next = 'table'
        if self.inside_table: next = 'tr'
        if self.inside_tr: next = 'td'
        return next

if __name__ == "__main__":
    print "*Come On"
    f = urllib2.urlopen('http://www.bolsamadrid.es/esp/mercados/acciones/accind1_1.htm')
    parser = StockParser()
    parser.feed(f.read())
    
    print pprint.pprint(parser.stocks)
    