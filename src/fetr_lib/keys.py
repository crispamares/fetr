import nltk
from nltk.tokenize import PunktWordTokenizer, PunktSentenceTokenizer

class NLAnalizer(object):
    es_stops = nltk.corpus.stopwords.words('spanish')
    model = {'Estados': 'np'}
    tagger = nltk.UnigramTagger(model=model, backoff = nltk.UnigramTagger(nltk.corpus.cess_esp.tagged_sents()))
    
    
    def extract_keywords(self, text, num=10):

        tokens = PunktWordTokenizer().tokenize(text) 
        fdist = nltk.FreqDist([w.lower() for w in tokens])
        
        key_words = []
        
        for w in fdist:
            if w not in self.es_stops and w.isalnum():
                key_words.append((w, fdist[w]))
            if len(key_words) > num: break
        
        return key_words
    
    def is_proper_noun(self, item):
        return (item[1] is None and (item[0].istitle() or item[0].isupper())) or (item[1] and item[1].startswith('np'))

    def get_nnp(self, original_text):
        sentences = PunktSentenceTokenizer().tokenize(original_text)
    
        list_of_NNPs = []
        for sentence in sentences:
            tokens = PunktWordTokenizer().tokenize(sentence)
            tagged =  self.tagger.tag(tokens)
    
            temp_npps = []
            for item in tagged:
                if self.is_proper_noun(item):
                    temp_npps.append(item[0])
                elif temp_npps:
                    list_of_NNPs.append(' '.join(temp_npps))
                    temp_npps = []

        return nltk.FreqDist(list_of_NNPs).items()

if __name__ == "__main__":
    import os, sys
    file_name = "/home/crispamares/proyectos/fetr/elpais2"
    
    with open(file_name, "r") as f:
        text = f.read()
    analizer = NLAnalizer()
    print analizer.get_nnp(text)