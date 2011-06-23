import nltk
from nltk.tokenize import PunktWordTokenizer 

def extract_keywords(text, num=10):

    es_stops = nltk.corpus.stopwords.words('spanish')
    
    tokens = PunktWordTokenizer().tokenize(text) 
    fdist = nltk.FreqDist([w.lower() for w in tokens])
    
    key_words = []
    
    for w in fdist:
        if w not in es_stops and w.isalnum():
            key_words.append((w, fdist[w]))
        if len(key_words) > num: break
    
    return key_words
