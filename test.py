import conf
from acquire_text import guardian_open_platform
from nlp import clean_text
from nlp import feature_extraction
from nlp import embedding
import pickle


__author__ = 'herve.schnegg'


url = conf.Guardian.URL
api_key = conf.Guardian.API_KEY
search = {"from-date":"2016-12-01"}
show = {"show-blocks":"body","show-tags":"all"}


# Retrieve a sample of article from Guardian Open API
corpus = guardian_open_platform.get_data(search, show, url, api_key, 10)


# Clean the articles
corpus = {k: {'article_body': v['article_body'], \
              'article_tags': v['article_tags'], \
              'cleaned_text': clean_text.clean_text(v['article_body'])} \
          for k, v in corpus.items()}


# Extract tfidf
vocabulary, tfidf = feature_extraction.extract_tfidf(map(lambda a: corpus[a]['cleaned_text'], corpus.keys()))
for k in range(tfidf.shape[0]):
    corpus[corpus.keys()[k]].update({"tfidf": tfidf[k,:]})

emb_add_tf = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='add', tf=True, idf=False, idf_vocabulary=vocabulary)
emb_avg_tf = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='avg', tf=True, idf=False, idf_vocabulary=vocabulary)
emb_add_tf_idf = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='add', tf=True, idf=True, idf_vocabulary=vocabulary)
emb_avg_tf_idf = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='avg', tf=True, idf=True, idf_vocabulary=vocabulary)
emb_add = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='add', tf=False, idf=False, idf_vocabulary=vocabulary)
emb_avg = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='avg', tf=False, idf=False, idf_vocabulary=vocabulary)
emb_add_idf = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='add', tf=False, idf=True, idf_vocabulary=vocabulary)
emb_avg_idf = embedding.retrieve_text_embedding(corpus[corpus.keys()[0]]['cleaned_text'], combine='avg', tf=False, idf=True, idf_vocabulary=vocabulary)

embedding.model.most_similar(positive=[emb_add_idf], topn=10)


# pickle.dump(corpus, open('data/corpus.dictionary.p', 'wb'))
# pickle.dump(vocabulary, open('data/vocabulary.list.p', 'wb'))
# corpus = pickle.load(open('data/corpus.dictionary.p', 'rb'))
# vocabulary = pickle.load(open('data/vocabulary.list.p', 'rb'))
