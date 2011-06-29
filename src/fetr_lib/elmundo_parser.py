'''
Created on 20/06/2011

@author: crispamares
'''

import html2text
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup

main_page = "http://www.elmundo.es"

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

    results = pool.findAll(['h2'])
    if not results:
        results = pool.findAll(['h1'])

    return results[0].text
    

def parse_article(url):
    f = urllib2.urlopen(url)
    html_text = f.read()

    head_line = parse_head_line(html_text)
    text = parse_body(html_text)
    
    return text, head_line


def parse_front_page():
    url = main_page+"/"

    f = urllib2.urlopen(url)
    html_text = f.read()
    f.close()
    
    pool = BeautifulSoup(html_text)

    results = pool.findAll('div', attrs={'class' : 'col col_01'})

    titles = results[0].findAll(['h2', 'h3', 'h4'])
    
    links = []
    for t in titles:
        l = t.find('a')
        if l:
            link = l['href']
        if link[:7] != "http://":
            link = main_page+link
        if link[-5:] == ".html" and (link[:29] == "http://www.elmundo.es/elmundo" or link[:29] == "http://www.elmundo.es/america"):
            links.append(link)
    return links

def _test_article():
    url = "http://www.elmundo.es/america/2011/06/20/estados_unidos/1308582993.html"
    url = "http://www.elmundo.es/america/2011/06/21/estados_unidos/1308690697.html"
    url = "http://elmundo.orbyt.es/2011/06/23/orbyt_en_elmundo/1308822185.html"
    url = "http://www.elmundo.es/elmundo/2011/06/23/internacional/1308825436.html"
    url = "http://www.elmundo.es/elmundo/2011/06/28/espana/1309278888.html"
    t, h = parse_article(url)

    print h,t

def _test_front_page():
    print parse_front_page()

if __name__ == '__main__':
    print "* El mundo"
    _test_article()
