import conf
import numpy as np
from gensim.models import word2vec


__author__ = 'schneggh'

'''
Use word2vec embeddings from Google
http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
'''


model = word2vec.Word2Vec.load_word2vec_format(conf.Word2Vec.GOOGLE_MODEL, binary=True)


def retrieve_word_embedding(word, model=model):
    empty_embedding = np.zeros(model.vector_size)
    try:
        embedding = model[word]
    except:
        embedding = empty_embedding
    return embedding


def retrieve_tfidf(word, vocabulary):
    try:
        tfidf = filter(lambda e: e[0] == word, vocabulary)[0][1]
    except:
        tfidf = 0
    return tfidf
    
    
def combine_addition(e1, e2):
    return e1 + e2


def combine_average(e1, e2):
    return np.mean([e1, e2], axis=0)


def retrieve_text_embedding(text, combine_fn=combine_addition, vocabulary=None, model=model):
    word_list = text.split()
    word_embedding = map(lambda w: retrieve_embedding(w, model), word_list)
    if vocabulary is not None:
        word_tfidf = np.array(map(lambda w: retrieve_tfidf(w, vocabulary), word_list))
        word_embedding = np.transpose(np.transpose(word_embedding) * word_tfidf)
    embedding = reduce(lambda e1, e2: combine_fn(e1, e2), word_embedding)
    return embedding



