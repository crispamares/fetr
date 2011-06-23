'''
Created on 20/06/2011

@author: crispamares
'''

import html2text
import keys
import urllib2

def parse_article(url):
    url += "?print=1"
    f = urllib2.urlopen(url)
    html_text = f.read().decode("latin-1").encode("utf-8")

    mark_down = html2text.html2text(html_text)

    mark_down = mark_down.replace("\n\n", "#fetr#").replace("\n","").replace("#fetr#", "\n")

    lines = mark_down.split("\n")
    text_lines = []
    head_line = ""
    for l in lines:
        if l and l[0].isalnum():
            text_lines.append(l)
        if l and l[0:2] == "# ":
            head_line = l[2:]
            
    text = "\n".join(text_lines)
    return keys.extract_keywords(text), head_line

if __name__ == '__main__':
    print "* El pais"

    url = "http://www.elpais.com/articulo/sociedad/WalMart/gana/mayor/pleito/discriminacion/sexual/historia/EE/UU/elpepusoc/20110620elpepusoc_13/Tes"
    url = "http://www.elpais.com/articulo/economia/UE/da/ultimatum/Grecia/apruebe/ajustes/elpepueco/20110620elpepueco_1/Tes"
    print parse_article(url)
