'''
Created on 20/06/2011

@author: crispamares
'''

import html2text
import keys
import urllib2
import HTMLParser

class MundoParser(HTMLParser.HTMLParser):

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.body = ""
        
        self.in_body = False
        self.div_number = 0

    def handle_starttag(self, tag, attrs):        
        if tag == "div" and dict(attrs).get("id") == "tamano":
            self.in_body = True
            self.div_number += 1
    
    def handle_endtag(self, tag):
        if tag == "div" and self.in_body:
            self.div_number -= 1
            if self.div_number == 0:
                self.in_body = False
    
    def handle_data(self, data):
        if self.in_body:
            self.body += data


def parse_body(html_text):
    pool = BeautifulSoup(html_text)
    
    
    results = pool.findAll('div', attrs={'id' : 'tamano'})
    paragraphs = results[0].findAll('p')
    text = ""
    for p in paragraphs:
        text += p.text+ "\n"
    return text
 
def parse_head_line(html_text):
    pool = BeautifulSoup(html_text)

    results = pool.findAll('h1')
    return results[0].text
    

def parse_article(url):
    f = urllib2.urlopen(url)
    html_text = f.read().decode("latin-1").encode("utf-8")

    parser = MundoParser()
    parser.feed(html_text)
    
    mark_down = html2text.html2text(html_text)
    body_mark_down = parser.body

    print body_mark_down

    mark_down = mark_down.replace("\n\n", "#fetr#").replace("\n"," ").replace("#fetr#", "\n")
    body_mark_down = body_mark_down.replace("\n\n", "#fetr#").replace("\n"," ").replace("#fetr#", "\n")

    lines = mark_down.split("\n")
    text_lines = []
    head_line = ""
    for l in lines:
        if l and l[0].isalnum():
            text_lines.append(l)
        if l and l[0:3] == "## ":
            head_line = l[3:]
        
    
    text = "\n".join(text_lines)
    return keys.extract_keywords(body_mark_down), head_line

if __name__ == '__main__':
    print "* El mundo"

    url = "http://www.elmundo.es/america/2011/06/20/estados_unidos/1308582993.html"
    print parse_article(url)
