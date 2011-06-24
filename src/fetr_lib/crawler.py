'''
Created on 23/06/2011

@author: crispamares
'''

import elpais_parser
import elmundo_parser
import expansion_parser
import cincodias_parser

class Crawler(object):
    def __init__(self):
        parsers_modules = []
        parsers_modules.append(elpais_parser)
        parsers_modules.append(elmundo_parser)
        parsers_modules.append(expansion_parser)
        parsers_modules.append(cincodias_parser)

        self.parsers = dict( map ( lambda x: (x.main_page, x), parsers_modules))        

    def get_front_pages_links(self):
        links = {}
        for page in self.parsers:
            l = self.parsers[page].parse_front_page()
            links[page] = l
        return links
    
    def run(self, links, errors=[]):
        '''
        @return: [[page, link, head_line, text, i]]
        '''
        papers = []
        for page in links:
            parser = self.parsers[page]
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
    c = Crawler()
    links = c.get_front_pages_links()
    papers = c.run(links)
    import pickle
    with open("/tmp/papers.pickle", "w") as f:
        pickle.dump(papers, f)
