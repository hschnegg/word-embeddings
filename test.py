import conf
from acquire_text import guardian_open_platform
from nlp import clean_text


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
