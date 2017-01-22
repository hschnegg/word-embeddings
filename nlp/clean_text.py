from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords


__author__ = 'herve.schnegg'


def clean_text(text, remove_stop_words=False):
    '''
    Perform basic text cleaning.
    :param text: Text to be cleaned
    :param remove_stop_words: Weather or not stop words are removed
    :return: Cleaned version of the text
    '''
    # remove html
    clean_text = BeautifulSoup(text, 'lxml').get_text()
    # remove some special characters
    clean_text = clean_text.replace(u'\xa0', u' ') \
                           .replace(u'\xa3', u' ') \
                           .replace(u'\u201d', u' ') \
                           .replace(u'\u201c', u' ') \
                           .replace(u'\u2019s', u' ') \
                           .replace(u'\u015f', u' ')
    # remove non letters
    clean_text = re.sub("[^a-zA-Z]"," ", clean_text)
    # remove multiple spaces between words
    clean_text = re.sub(' +',' ', clean_text)
    # convert to lower case
    clean_text = clean_text.lower()
    if remove_stop_words:
        stops = set(stopwords.words("english"))
        clean_text = ' '.join([word for word in clean_text.split(' ') if word not in stops])
    return clean_text
