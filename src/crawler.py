'''
Created on 23/06/2011

@author: crispamares
'''

import elpais_parser
import elmundo_parser
import expansion_parser
import cincodias_parser


def get_front_pages_links(parsers):
    links = {}
    for page in parsers:
        l = parsers[page].parse_front_page()
        print page, "Done", len(l)
        links[page] = l
    return links

if __name__ == '__main__':
    print "* Robot"
    parsers_modules = []
    parsers_modules.append(elpais_parser)
    parsers_modules.append(elmundo_parser)
    parsers_modules.append(expansion_parser)
    parsers_modules.append(cincodias_parser)

    parsers = dict( map ( lambda x: (x.main_page, x), parsers_modules))        
    
    links = get_front_pages_links(parsers)
    print links
    
    for page in links:
        parser = parsers[page]
        for link in links[page]:
            try:
                text, head_line = parser.parse_article(link)
                #print link, "Done", head_line
            except:
                print "ERROR::", link
            
