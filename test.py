import conf
from acquire_text import guardian_open_platform
from nlp import clean_text


url = conf.Guardian.URL
api_key = conf.Guardian.API_KEY
search = {"from-date":"2016-12-01"}
show = {"show-blocks":"body","show-tags":"all"}


corpus = guardian_open_platform.get_data(search, show, url, api_key, 10)
