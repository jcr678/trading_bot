import pandas as pd
import xml
import bs4
import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import time as time_right_now
import sentiment

stocks_list = ['TSLA', 'GOOGL', 'AAPL', 'MSFT', 'BABA']
stock_dict = {}
columns = ['Date', 'Time', 'Price', '50-Day MA', '200-Day MA', 'Market Open', 'Prev Close', 'Trading Volume', 'Sentiment', 'Subjectivity']
for stock in stocks_list:
    stock_dict[stock] = pd.DataFrame(columns = columns)

base_url = 'https://finance.yahoo.com/quote/'
rest_of_url = '?p='

def scrape(stocks = stocks_list, dictionary = stock_dict):
    for ticker in stocks_list:
        url = base_url + ticker + rest_of_url + ticker
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        print(ticker + ": " + url)

        key_stats_url = base_url + ticker + '/key-statistics' + rest_of_url + ticker
        key_stats_req = requests.get(key_stats_url)
        stats_soup = bs4.BeautifulSoup(key_stats_req.text, 'lxml')

        # date/time
        now = datetime.datetime.now(pytz.timezone('US/Central'))
        date = now.strftime("%b %d, %Y")
        time = now.strftime("%H:%M")

        # price
        price = float( soup.find("div", {'class':"My(6px) Pos(r) smartphone_Mt(6px)"}).find('span').text.replace(',', '') )

        # Moving Averages
        fifty_day_SMA = float( stats_soup.find_all("tr" , {"class":"Bxz(bb) H(36px) BdB Bdbc($seperatorColor)"})[4].find("td", {"class": "Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)"}).text.replace(",", '') )
        t_hundred_day_SMA = float( stats_soup.find_all("tr" , {"class":"Bxz(bb) H(36px) BdB Bdbc($seperatorColor)"})[5].find("td", {"class": "Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)"}).text.replace(",", '') )

        # market open/close
        m_open = float( soup.find_all("td", {"class":"Ta(end) Fw(600) Lh(14px)"})[1].find('span').text.replace(',', '') )
        p_close = float( soup.find_all("td", {"class":"Ta(end) Fw(600) Lh(14px)"})[0].find('span').text.replace(',', '') )

        # volume
        volume = float( soup.find_all("td", {"class":"Ta(end) Fw(600) Lh(14px)"})[6].find('span').text.replace(',', '') )

        # sentiment
        analyze = sentiment.Analysis(ticker);
        sent, subj = analyze.run()

        # append info
        entry = [date, time, price, fifty_day_SMA, t_hundred_day_SMA, m_open, p_close, volume, sent, subj]
        stock_dict[ticker] = stock_dict[ticker].append(pd.Series(entry, index=columns), ignore_index=True)


def display_information(stocks = stocks_list, dictionary = stock_dict):
    for ticker in stocks_list:
        print(ticker + ": ")
        pd.options.display.max_columns = 13
        print(stock_dict[ticker])
        print("*" * 30)
        print("*" * 30, '\n')
