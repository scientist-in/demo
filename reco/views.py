from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib
import ipdb
import requests
from django import template
import json
import os
from time import sleep
import pandas as pd
import ipdb
import re
# Create your views here.
def index(request):
    return render_to_response(
        'reco/index.html',
        context_instance=RequestContext(request)
    )

def search(request):
    
    #ipdb.set_trace()
    words = request.GET.get('search_term')
    
    words_url_encoded = urllib.quote_plus(words)
    if os.getcwd() == '/home/keeda/Documents/scientist/demo/recosys/demo':
        solr_query = u"http://192.168.0.102:8983/solr/recosys/select?indent=on&q="+words_url_encoded+"&wt=json"
    else:
        solr_query = u"http://54.83.149.27:8983/solr/recosys/select?indent=on&q="+words_url_encoded+"&wt=json"
    response_from_search = requests.get(solr_query)
    jsonRes = response_from_search.json()
    jsonRes = jsonRes['response']['docs']
    search_len = len(jsonRes)
    if search_len>5:
        jsonRes = jsonRes[0:5]
        search_len = range(5)
    else:
        search_len = range(search_len)
    movie_id = [str(i['movieId'][0]) for i in jsonRes]
    movie_title = [str(i['title'][0]) for i in jsonRes]
    
    
    
    return render_to_response('reco/search_results.html',{'movie_id':movie_id,'movie_title':movie_title,'search_len':search_len})

def get_recommendations(request):
    user_liked = request.GET.get('user_liked')
    #ipdb.set_trace()
    with open('user_liked.json', 'w') as outfile:
            json.dump(user_liked, outfile)
    os.system("screen -S recosys -p 0 -X stuff \"run\\n\"")
    while not os.path.isfile('recommendations.json'):
            pass
    sleep(.3)
    with open('recommendations.json', 'r') as infile:
        recommendations = json.load(infile)
        recommendations = str(recommendations)
        recommendations = json.loads(recommendations)
    #ipdb.set_trace()
    movie_id = recommendations['movieId']
    movie_title = recommendations['title']
    recommendations_len = range(len(movie_id))
    return render_to_response('reco/recommendations.html',{'movie_id':movie_id,'movie_title':movie_title,'recommendations_len':recommendations_len})
def get_recommendations_nlp(request):
    user_liked = request.GET.get('user_liked')
    #ipdb.set_trace()
    with open('user_liked.json', 'w') as outfile:
            json.dump(user_liked, outfile)
    #os.system("screen -S recosys -p 0 -X stuff \"run\\n\"")
    #while not os.path.isfile('recommendations.json'):
    #        pass
    #sleep(.3)
    #logic to tags for those movies
    #ipdb.set_trace()
    #os.getcwd()
    user_liked = [ int(i) for i in re.sub(r"\[|]","",user_liked).split(',')]
    df = pd.read_csv(os.getcwd()+'/reco/tags.csv')
    df = df.loc[[int(i) in user_liked for i in df['movieId']]]['tag']
    df = [re.sub(r"\n","",i) for i in df]
    all_tags = ''.join(str(i) for i in df)
    all_tags_encoded = urllib.quote_plus(all_tags)
    if len(all_tags_encoded)>1990:
        if all_tags_encoded[1990]=='+':
            all_tags_encoded = all_tags_encoded[0:1989]
        else:
            all_tags_encoded = all_tags_encoded[0:1990]
    if os.getcwd() == '/home/keeda/Documents/scientist/demo/recosys/demo':
        solr_query = u"http://192.168.0.102:8983/solr/reconlp/select?indent=on&q="+all_tags_encoded+"&wt=json"
    else:
        solr_query = u"http://54.83.149.27:8983/solr/reconlp/select?indent=on&q="+all_tags_encoded+"&wt=json"
    response_from_search = requests.get(solr_query)
    jsonRes = response_from_search.json()
    jsonRes = jsonRes['response']['docs']
    reco_len = len(jsonRes)
    if reco_len>10:
        jsonRes = jsonRes[0:10]
        reco_len = range(10)
    
    #ipdb.set_trace()
    movie_id = [i['movieId'][0] for i in jsonRes]
    movies = pd.read_csv(os.getcwd()+'/reco/movies.csv')
    recommendations = movies.loc[[i in movie_id for i in movies['movieId']]][['movieId','title']]
    #recommendations = recommendations.to_json()
    movie_title = recommendations['title']
    movie_id = recommendations['movieId']
    recommendations_len = range(len(movie_id))
    #http://54.83.149.27:8983/solr/recosys/update?stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E
    return render_to_response('reco/recommendations_nlp.html',{'movie_id':movie_id,'movie_title':movie_title,'recommendations_len':recommendations_len})
