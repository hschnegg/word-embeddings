import numpy as np
from gensim.models import word2vec


__author__ = 'schneggh'

'''
Use word2vec embeddings from Google
http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
'''


model = word2vec.Word2Vec.load_word2vec_format('data/GoogleNews-vectors-negative300.bin', binary=True)


def retrieve_word_embedding(word, model=model):
    empty_embedding = np.zeros(model.vector_size)
    try:
        embedding = model[word]
    except:
        embedding = empty_embedding
    return embedding


def retrieve_text_embedding(text, model=model):
    word_list = text.split()
    embedding = reduce(lambda e1, e2: e1 + e2, map(lambda w: retrieve_embedding(w, model), word_list))
    return embedding
