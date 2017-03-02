import conf
import numpy as np
from gensim.models import word2vec


__author__ = 'schneggh'

'''
Use word2vec embeddings from Google
http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
'''


google_model = conf.Word2Vec.GOOGLE_MODEL
model = word2vec.Word2Vec.load_word2vec_format(google_model, binary=True)


def retrieve_word_embedding(word, model=model):
    try:
        embedding = model[word]
    except:
        empty_embedding = np.zeros(model.vector_size)
        embedding = empty_embedding
    return embedding


def retrieve_word_idf(word, vocabulary):
    try:
        idf = filter(lambda e: e[0] == word, vocabulary)[0][1]
    except:
        idf = 0
    return idf


def retrieve_word_idf_embedding(word, idf_vocabulary, model=model):
    embedding = retrieve_word_embedding(word, model=model)
    idf = retrieve_word_idf(word, idf_vocabulary)
    idf_embedding = idf * embedding
    return idf_embedding


def combine_addition(e1, e2):
    return e1 + e2


def combine_average(e1, e2):
    return np.mean([e1, e2], axis=0)


def retrieve_text_embedding(text, combine='add', tf=True, idf=False, idf_vocabulary=None, model=model):
    word_list = text.split()
    if not tf:
        word_list = np.unique(word_list)
    if idf:
        word_embedding = map(lambda w: retrieve_word_idf_embedding(w, idf_vocabulary, model), word_list)
    else:
        word_embedding = map(lambda w: retrieve_word_embedding(w, model), word_list)
    if combine == 'add':
        combine_fn = combine_addition
    else:
        combine_fn = combine_average
    embedding = reduce(lambda e1, e2: combine_fn(e1, e2), word_embedding)
    return embedding



