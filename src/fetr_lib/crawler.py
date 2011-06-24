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
    
def run(errors=[]):
    '''
    @return: [[page, link, head_line, text, i]]
    '''
    parsers_modules = []
    parsers_modules.append(elpais_parser)
    parsers_modules.append(elmundo_parser)
    parsers_modules.append(expansion_parser)
    parsers_modules.append(cincodias_parser)

    parsers = dict( map ( lambda x: (x.main_page, x), parsers_modules))        
    
    links = get_front_pages_links(parsers)
    
    papers = []
    for page in links:
        parser = parsers[page]
        i = 0
        for link in links[page]:
            try:
                text, head_line = parser.parse_article(link)
                papers.append([page, link, head_line, text, i])
                i += 0
            except:
                errors.append(link)
            
    return papers

if __name__ == '__main__':
    print "* Robot"
    papers = run()
    import pickle
    with open("/tmp/papers.pickle", "w") as f:
        pickle.dump(papers, f)
