from flask import (Flask, request, jsonify)
from newsapi import NewsApiClient
import json
import re, collections
									 
application = Flask(__name__)


@application.route('/')
def index():
		return application.send_static_file('page2.html')

@application.route('/query', methods = ['GET'])
def ajax_request():
		newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')
		
		keyword = request.args.get('keyword',"")
		fromDate = request.args.get('fromDate',"")
		toDate = request.args.get('toDate',"")
		category = request.args.get('category',"")
		source = request.args.get('source',"")
		if source == 'all':
			source = ''
		if source=="null":
			source=None
		try:
			all_articles = newsapi.get_everything(q=keyword,sources=source,from_param=fromDate,to=toDate,language='en',sort_by='publishedAt')
		except Exception as e:
			errorMsg = {'status':'error','err':e.get_message()}
			return json.dumps(errorMsg)
		
		return jsonify(all_articles=all_articles)
				

@application.route('/extraCards', methods = ['GET'])
def extraCards_request():
		newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')

		keyword = request.args.get('keyword',"")
		fromDate = request.args.get('fromDate',"")
		toDate = request.args.get('toDate',"")
		category = request.args.get('category',"")
		source = request.args.get('source',"")
		all_articles = newsapi.get_everything(q=keyword,sources=source,from_param=fromDate,to=toDate,language='en',sort_by='publishedAt')

		return jsonify(all_articles=all_articles)


@application.route('/sourceData', methods = ['GET'])
def sourceData_request():
		newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')

		category = request.args.get('category',"")
		
		if category=="all":
			source_articles = newsapi.get_sources(language='en',country='us')
		else:
			source_articles = newsapi.get_sources(category=category,language='en',country='us')

		return jsonify(source_articles=source_articles)

@application.route('/slidingWindow', methods = ['GET'])
def slidingWindowRequest():
		newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')

		sliding_headlines = newsapi.get_top_headlines(language='en')

		return jsonify(sliding_headlines=sliding_headlines)

def strip_word(str):
	return str.strip()

@application.route('/wordCloud', methods = ['GET'])
def wordCloudRequest():
	newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')
	headlines = newsapi.get_top_headlines(page_size=30,language='en')
	maxCount1=1
	maxCount2=2
	listOfArticlesToSend = []
	flag = True
	counterIdx = 1
	counterIdx2= 5
	if counterIdx<counterIdx2:
		stopwordsInFile = open("stopwords_en.txt","r")
	x1=9
	x2=4
	articlesAll = headlines['articles']
	if x1>x2:
		all_stopword = stopwordsInFile.readlines()
	all_stopwords = []
	ctr = 0
	while True:
		if ctr >= len(articlesAll):
			break
		stringTitle = articlesAll[ctr]
		title_Articles = stringTitle['title']
		ui,us=99,999
		titleHeadlines = re.sub(r'[^\w\s]','',title_Articles)
		listOfArticlesToSend += [capital_new_title.lower() for capital_new_title in titleHeadlines.split()]
		ctr += 1
	count = collections.Counter(listOfArticlesToSend)
	ctr2 = 0
	while True:
		if ctr2 >= len(all_stopword):
			break
		all_stopwords.append(strip_word(all_stopword[ctr2]))
		ctr2 += 1
	for i in range(len(all_stopwords)):
		if all_stopwords[i] in count.keys() and maxCount1<maxCount2 and flag==True:
			del count[all_stopwords[i]]
		elif all_stopwords[i].capitalize() in count.keys():
			del count[all_stopwords[i].capitalize()]
	top_30 = count.most_common(30)
	return json.dumps(top_30)

@application.route('/cnnCards', methods = ['GET'])
def cnnCardsRequest():
		newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')

		top_headlines = newsapi.get_top_headlines(sources='cnn',language='en')


		# print(top_headlines)
		return jsonify(top_headlines=top_headlines)

@application.route('/foxCards', methods = ['GET'])
def foxCardsRequest():
		newsapi = NewsApiClient(api_key='dd11016d7a634fb2aa274de652a321c7')

		top_headlines = newsapi.get_top_headlines(sources='fox-news',language='en')


		# print(top_headlines)
		return jsonify(top_headlines=top_headlines)


		
		
if __name__ == "__main__":
		application.run(debug = True)