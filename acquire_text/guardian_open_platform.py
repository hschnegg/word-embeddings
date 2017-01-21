__author__ = 'herve.schnegg'


'''
Resource required to retrieve content from the Guardian Open Platform
http://open-platform.theguardian.com/
'''

from __future__ import division
import requests
import math


def format_tags(tags):
    '''
    Format the tags element returned by the api
    '''
    tag_dict = {}
    for t in tags:
        tag_type = t['type']
        tag_id = t['id']
        tag_dict.setdefault(tag_type, []).append(tag_id)
    return tag_dict
    

def format_body(body):
    '''
    Combine the body elements retrieved by the api
    '''
    text = ''
    for b in body:
        t = b['bodyTextSummary']
        text += t
    return text


def retrieve_article_details(res):
    '''
    Retrieve the required body and tags elements from the api
    '''
    article_body = format_body(res['blocks']['body'])
    article_tags = format_tags(res['tags'])
    article_dict = {"article_body": article_body, "article_tags": article_tags}
    return article_dict


def query_open_guardian(search, show, url, api_key, limit):
    '''
    Run a query against the api and format the result as a dictionary keyd by article id
    '''
    payload = search.copy()
    corpus = {}
    payload.update({"api-key": api_key})
    
    try:
        response = requests.request("GET", url, params=payload).json()['response']
        last_page = response['pages']
        article_by_page = response['pageSize']
        page_to_retrieve = math.ceil(limit / article_by_page)
        page_to_retrieve = int(page_to_retrieve if page_to_retrieve <= last_page else last_page)
    except:
        page_to_retrieve = 0
        print 'e1'
        
    for page in range(1, page_to_retrieve + 1):
        payload.update({"page": page})
        payload.update(show)

        try:
            response = requests.request("GET", url=url, params=payload).json()['response']
            results = response['results']
        except:
            results = []
            print 'e2'
            
        for r in results:
            article_id = r['id']
            article_details = retrieve_article_details(r)
            corpus.update({article_id: article_details})

    return corpus


# # Sample call

# url = "http://content.guardianapis.com/search"
# api_key = "6e82579f-4697-4bf8-9619-73cdd14e968f"
# search = {"from-date":"2016-12-01"}
# search = {"tag":"technology/artificialintelligenceai"}
# show = {"show-blocks":"body","show-tags":"all"}

# corpus = query_open_guardian(search, show, url, api_key, 20)
