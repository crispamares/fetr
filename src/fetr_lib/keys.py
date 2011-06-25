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

'''
 @name get_nnp_ngrams
 @author: jonhurlock - http://sucs.org/~jonhurlock
 @date - 2011-01-30

 This is a function which prints out a list of unique ngrams based
 of strings of NNPs (Proper Nouns) which are next to each other.
 Requires: NLTK - www.nltk.org/ & itertools (Should be bundled with python)
 Outputs: A list of unique lists of ngrams found from the input
 Input: @original_text = A string of text you want to search for NNPs
       @highlight = An int, the maxium sized ngram you wish to search for, Recommend not bigger 
        than 3, but must be smaller than number of words in @original_text
       @minsize = An int, the minimum sized ngram you want.
'''
def get_nnp_ngrams(original_text, highlight=3, minsize=0):
    """
        Search @input orginial_text for ngrams of proper nouns 
        and return a list of relevant ngrams, read the comments
        above the function/method declaration as wo what each
        input does.
    """
    minsize = minsize-1
    if minsize<0:
        minsize = 0 

    tokens = PunktWordTokenizer().tokenize(original_text)
    
    tagger = nltk.UnigramTagger(nltk.corpus.cess_esp.tagged_sents()) 
    #tagger = nltk.UnigramTagger(nltk.corpus.conll2007.tagged_sents())
    
    tagged =  tagger.tag(tokens)
    
    new_tagged = []
    for item in tagged:
        if item[1] is None and (item[0].istitle() or item[0].isupper()):
            new_tagged.append((item[0], "np"))
        else:
            new_tagged.append(item)
    
    tagged = new_tagged
    
    print new_tagged
    #for word in tagged:
    #   print word
    doc_length = len(tokens)
    counter = 0
    counter2 = 0
    if highlight==0:
        concated_test = doc_length # This is set to doc_length but could be anything recommend 3.
    else:
        concated_test = highlight
    list_of_NNPs = []
    while counter < (doc_length-1):
        while counter2 < concated_test:
            counter2 = counter2+1
            counter3 = 0
            #print '--------------------'
            temp_array = []
            all_nnp = True
            while counter3 < counter2:
                if counter < (doc_length-counter3):
                    #print tokens[counter+counter3],tagged[counter+counter3][1]
                    temp_array.append(tokens[counter+counter3])
                    if not tagged[counter+counter3][1] or not tagged[counter+counter3][1].startswith("np"):
                        all_nnp = False
                counter3 = counter3+1
            counter3 = 0
            if all_nnp == True:
                if(len(temp_array)>minsize):
                    list_of_NNPs.append(temp_array)
                #print 'added to main array'
            #else:
                #print 'not all NNPs'
        counter2 = 0
        counter = counter+1
    #for ngram in list_of_NNPs:
    #   print ngram
    import itertools
    list_of_NNPs.sort()
    unique_NNPs = list(list_of_NNPs for list_of_NNPs,_ in itertools.groupby(list_of_NNPs))
    #for ngram in unique_NNPs:
    #   print ngram
    return unique_NNPs

if __name__ == "__main__":
    import os, sys
    file_name = "/home/crispamares/proyectos/fetr/elpais"
    with open(file_name, "r") as f:
        text = f.read()
    print get_nnp_ngrams(text, 2, 1)