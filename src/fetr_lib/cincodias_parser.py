'''
Created on 20/06/2011

@author: crispamares
'''

import keys
import urllib2
from BeautifulSoup import BeautifulSoup

main_page = "http://www.cincodias.com"

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

    contenido = pool.find('div', attrs={'id' : 'contenido'})
    results = contenido.findAll(['h1','h2'])
    return results[0].text
    
    

def parse_article(url):
    f = urllib2.urlopen(url)
    html_text = f.read()

    head_line = parse_head_line(html_text)
    text = parse_body(html_text)
    
    return text, head_line

def parse_front_page():
    url = main_page + "/"
    f = urllib2.urlopen(url)
    html_text = f.read()
    f.close()
    
    pool = BeautifulSoup(html_text)
    
    contenido = pool.find('div', attrs={'id' : 'contenido'})
    divs = [contenido.findAll('div')[1]]
    divs.append(divs[0].findNextSibling())
    
    links = []
    for div in divs:
        titles = div.findAll('h2')

        for t in titles:
            link = t.find('a')['href']
            if link[:7] != "http://":
                link = main_page+link
            links.append(link)
    
    return links

def _test_article():
    url = "http://www.cincodias.com/articulo/mercados/banca-alarga-anos-hipotecas-reconocer-impagos/20110623cdscdimer_2/"
    url = "http://www.cincodias.com/articulo/empresas/industria-espanola-falla-comercializacion/20110623cdscdiemp_21/"
    url = "http://www.cincodias.com/articulo/opinion/reino-unido-isla/20110623cdscdiopi_7/"
    print parse_article(url)

def _test_front_page():
    print parse_front_page()
    
if __name__ == '__main__':
    print "* Cinco dias"

    print _test_front_page()
