'''
Created on 23/06/2011

@author: crispamares
'''

import urllib2
from BeautifulSoup import BeautifulSoup

def parser_stocks(url):
    '''
    @return: [Last, Diff, Time, Volume]
    '''
    f = urllib2.urlopen(url)
    html_text = f.read()
    f.close()

    #
    # The web has some errors    
    html_text = "<html><head></head>"+html_text[html_text.find('body'):]

#    parser = LiveStockParser()
#    parser.feed(html_text)
    pool = BeautifulSoup(html_text)
    table = pool.find("table", attrs={'width' : '300', 'align' : 'center'})
    values = table.findAll("td", attrs={'align' : 'Right'})
    
    results = []  
    results.append(float(values[0].text.replace(".","").replace(",",".")))
    results.append(float(values[1].text.replace("%","").replace(",",".")))
    results.append(values[2].text)
    results.append(float(values[3].text.replace(".","").replace(",",".")))
    
    return results


if __name__ == "__main__":
    url = 'http://www.pcbolsa.com/movil/MovilCotizacion.aspx?ISIN=ES0178430E18&CodIndi=x&Plaza=55&Cotizacion=TELEFONICA'
    print parser_stocks(url)
    
    