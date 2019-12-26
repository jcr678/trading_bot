import xml
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

class Analysis:
	def __init__(self, term):
		self.term = term
		self.sentiment = 0
		self.subjectivity = 0
		self.url = 'https://news.search.yahoo.com/search?p=' + self.term + '&fr=uh3_news_vert_gs&fr2=p%3Anews%2Cm%3Asb'

	def run(self):
		response = requests.get(self.url)
		soup = BeautifulSoup(response.text, 'lxml')
		headline_results = soup.find_all("a",{"style" : "font-size:16px;"})
		for text in headline_results:
			# print(text.get_text())
			blob = TextBlob(text.get_text())

			self.sentiment += blob.sentiment.polarity / len(headline_results)
			self.subjectivity += blob.sentiment.subjectivity / len(headline_results)

			# print(self.sentiment)
			# print(self.subjectivity)

		return self.sentiment, self.subjectivity
