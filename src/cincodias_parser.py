'''
Created on 20/06/2011

@author: crispamares
'''

import keys
import urllib2
from BeautifulSoup import BeautifulSoup

def parse_body(html_text):
    pool = BeautifulSoup(html_text)
    
    
    results = pool.findAll('div', attrs={'class' : 'txt_noticia'})

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
    
    results = pool.findAll('div', attrs={'id' : 'mod_9770'})
    titles = results[0].findAll('h2')
    
    links = []
    for t in titles:
        link = t.find('a')['href']
        if link[:7] != "http://":
            link = "http://www.cincodias.com"+link
        links.append(link)
    
    return links

def _test_article():
    url = "http://www.cincodias.com/articulo/mercados/banca-alarga-anos-hipotecas-reconocer-impagos/20110623cdscdimer_2/"
    f = urllib2.urlopen(url)
    html_text = f.read()

    head_line = parse_head_line(html_text)
    body = parse_body(html_text)
    print head_line
    print body
    print keys.extract_keywords(body)

def _test_front_page():
    url = "http://www.cincodias.com"
    f = urllib2.urlopen(url)
    html_text = f.read()
    
    print parse_front_page(html_text)
    
if __name__ == '__main__':
    print "* Cinco dias"

    print _test_front_page()
