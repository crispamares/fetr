'''
Created on 20/06/2011

@author: crispamares
'''

import keys
import urllib2
from BeautifulSoup import BeautifulSoup

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
    
    
    
def parse_front_page(html_text):
    pool = BeautifulSoup(html_text)

    results = pool.findAll('div', attrs={'class' : 'bloque destacado ancho_cuerpo'})
    results2 = pool.findAll('div', attrs={'class' : 'bloque ancho_cuerpo'})
    
    titles = results[0].findAll(['h1', 'h2']) + results2[0].findAll('h2')
    
    links = []
    for t in titles:
        link = t.find('a')['href']
        if link[:7] != "http://":
            link = "http://www.expansion.com"+link
        if link[-5:] == ".html":
            links.append(link)
    return links

def _test_article():
    url = "http://www.expansion.com/2011/06/23/empresas/banca/1308782147.html"
    f = urllib2.urlopen(url)
    html_text = f.read()

    head_line = parse_head_line(html_text)
    body = parse_body(html_text)
    print head_line
    print body
    print keys.extract_keywords(body)

def _test_front_page():
    url = "http://www.expansion.com/"
    f = urllib2.urlopen(url)
    html_text = f.read()
    
    print parse_front_page(html_text)

if __name__ == '__main__':
#    print "* Expansion"
    print _test_front_page()
    
    