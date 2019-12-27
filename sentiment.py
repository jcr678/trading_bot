import xml
import requests
import re
from bs4 import BeautifulSoup
from textblob import TextBlob

class Analysis:
    def __init__(self, term):
        self.term = term
        self.sentiment = 0
        self.subjectivity = 0
        self.url = 'https://news.search.yahoo.com/search?p=' + self.term + '&fr=uh3_news_vert_gs&fr2=p%3Anews%2Cm%3Asb'
        self.candlestick = -1 
		self.url = 'https://news.search.yahoo.com/search?p=' + self.term + '&fr=uh3_news_vert_gs&fr2=p%3Anews%2Cm%3Asb'
		self.urlCandleStick = 'https://www.hotcandlestick.com/' + self.term
		#https://www.hotcandlestick.com/candles.htm
		self.candlestick_dict = {
			"Bullish Mat Hold": 1,
			"Bullish Rising Three Methods": 2,
			"Bullish Rising 3 Methods": 2,
			"Bullish Separating Lines": 3,
			"Bullish Side-By-Side White Lines": 4,
			"Bullish Three-Line Strike": 5,
			"Bullish 3-Line Strike": 5,
			"Bullish Upside Gap Three Methods": 6,
			"Bullish Upside Gap 3 Methods": 6,
			"Bullish Upside Tasuki Gap": 7,
			"Bullish Abandoned Baby": 8,
			"Bullish Belt Hold": 9,
			"Bullish Breakaway": 10,
			"Bullish Concealing Baby Swallow": 11,
			"Bullish Doji Star": 12,
			"Bullish Engulfing": 13,
			"Bullish Hammer": 14,
			"Bullish Harami": 15,
			"Bullish Harami Cross": 16,
			"Bullish Homing Pigeon": 17,
			"Bullish Inverted Hammer": 18,
			"Bullish Kicking": 19,
			"Bullish Ladder Bottom": 20,
			"Bullish Matching Low": 21,
			"Bullish Meeting Lines": 22,
			"Bullish Morning Doji Star": 23,
			"Bullish Morning Star": 24,
			"Bullish Piercing Line": 25,
			"Bullish Stick Sandwich": 26,
			"Bullish Three Inside Up": 27,
			"Bullish Three Outside Up": 28,
			"Bullish Three Stars in the South": 29,
			"Bullish Three White Soldiers":30,
			"Bullish 3 Inside Up": 27,
			"Bullish 3 Outside Up": 28,
			"Bullish 3 Stars in the South": 29,
			"Bullish 3 White Soldiers":30,
			"Bullish Tri-Star":31,
			"Bullish Tweezer Bottom": 32,
			"Bullish Unique Three River Bottom":33,
			"Bearish Downside Gap Three Methods": 34,
			"Bullish Unique 3 River Bottom":33,
			"Bearish Downside Gap 3 Methods": 34,
			"Bearish Downside Tasuki Gap": 35,
			"Bearish Falling Three Methods": 36,
			"Bearish Falling 3 Methods": 36,
			"Bearish In-Neck":37,
			"Bearish On-Neck":38,
			"Bearish Separating Lines":39,
			"Bearish Side-By-Side White Lines":40,
			"Bearish Three-Line Strike":41,
			"Bearish 3-Line Strike":41,
			"Bearish Thrusting": 42,
			"Bearish Abandoned Baby": 43,
			"Bearish Advance Block": 44,
			"Bearish Belt Hold": 45,
			"Bearish Breakaway": 46,
			"Bearish Dark Cloud Cover": 47,
			"Bearish Deliberation": 48,
			"Bearish Doji Star": 49,
			"Bearish Engulfing": 50,
			"Bearish Evening Doji Star": 51,
			"Bearish Evening Star": 52,
			"Bearish Hanging Man": 53,
			"Bearish Harami": 54,
			"Bearish Harami Cross": 55,
			"Bearish Identical Three Crows": 56,
			"Bearish Identical 3 Crows": 56,
			"Bearish Kicking": 57,
			"Bearish Meeting Lines": 58,
			"Bearish Shooting Star": 59,
			"Bearish Three Black Crows": 60,
			"Bearish Three Inside Down": 61,
			"Bearish Three Outside Down": 62,
			"Bearish 3 Black Crows": 60,
			"Bearish 3 Inside Down": 61,
			"Bearish 3 Outside Down": 62,
			"Bearish Tri-Star": 63,
			"Bearish Tweezer Top": 64,
			"Bearish Two Crows": 65,
			"Bearish Upside Gap Two Crows":66,
			"Bearish 2 Crows": 65,
			"Bearish Upside Gap 2 Crows":66
			}

    def run(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        headline_results = soup.find_all("a",{"style" : "font-size:16px;"})
        for text in headline_results:
            # print(text.get_text())
            blob = TextBlob(text.get_text())

            self.sentiment += blob.sentiment.polarity / len(headline_results)
            self.subjectivity += blob.sentiment.subjectivity / len(headline_results)
        return self.sentiment, self.subjectivity
            # print(self.sentiment)
            # print(self.subjectivity)
    def run_candlestick(self):
        responseCandleStick = requests.get(self.urlCandleStick)
	soup = BeautifulSoup(responseCandleStick.text, 'html5')
	headline_result = soup.find('div', {'id':'dailypattern'})
	#print(re.findall(r'"([^"]*)"', str(headline_result))[3])
	candleStickString = re.findall(r'"([^"]*)"', str(headline_result))[3]
	if candleStickString in self.candlestick_dict:
		self.candlestick = float(self.candlestick_dict[candleStickString])/66.0 #normalize between 0 and 1
	else:
		print("ERROR!!!!") #candlestick does not exist in dict
	 	self.candlestick = -1
	#print(self.candlestick)
        return self.candlestick
