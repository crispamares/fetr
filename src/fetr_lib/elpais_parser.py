'''
Created on 20/06/2011

@author: crispamares
'''

import html2text
import keys
import urllib2
from BeautifulSoup import BeautifulSoup

main_page = "http://www.elpais.com"

def parse_article(url):
    if url[-4:] == "/Tes":
        return parse_article_std(url)
    else:
        return parse_article_pol(url)


def parse_article_std(url):
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
    return text, head_line

def parse_article_pol(url):
    f = urllib2.urlopen(url)
    html_text = f.read()
    
    pool = BeautifulSoup(html_text)
    
    results = pool.findAll('div', attrs={'id' : 'cuerpo_noticia'})
    paragraphs = results[0].findAll('p')
    text = ""
    for p in paragraphs:
        text += p.text+ "\n"

    head_line_res = pool.findAll('h1')
    head_line = head_line_res[0].text

    return text, head_line

def parse_front_page():
    url = main_page +"/"
    f = urllib2.urlopen(url)
    html_text = f.read()
    f.close()
    
    pool = BeautifulSoup(html_text)

    results = pool.findAll('div', attrs={'class' : "estructura_2col_1zq"})
    
    titles = results[0].findAll('h2')
    
    links = []
    for t in titles:
        link = t.find('a')['href']
        if link[:7] != "http://":
            link = main_page+link
        if (link[-5:] == ".html" or link[-4:] == "/Tes") and not link.startswith("http://blogs.elpais.com/"):
            links.append(link)
    return links


def _test_article_std():
    url = "http://www.elpais.com/articulo/internacional/Obama/anuncia/EE/UU/repliega/Afganistan/forma/gradual/elpepuint/20110623elpepuint_1/Tes"
    print parse_article_std(url)

def _test_article_pol():
    url = "http://politica.elpais.com/politica/2011/06/23/actualidad/1308813814_352195.html"
    print parse_article_pol(url)

def _test_article():
    url = "http://www.elpais.com/articulo/internacional/Obama/anuncia/EE/UU/repliega/Afganistan/forma/gradual/elpepuint/20110623elpepuint_1/Tes"
    url2 = "http://politica.elpais.com/politica/2011/06/23/actualidad/1308813814_352195.html"
    url2 = "http://politica.elpais.com/politica/2011/06/22/actualidad/1308772934_025752.html"
    url = "http://www.elpais.com/articulo/deportes/Alonso/marca/paso/Valencia/elpepudep/20110624elpepudep_11/Tes"
    print parse_article(url)

def _test_front_page():
    url = "http://www.elpais.com/"
    print parse_front_page(url)

if __name__ == '__main__':
    print "* El pais"

    _test_article()

    