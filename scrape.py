import get_data
import bs4
import requests
import pandas as pd
import datetime
import pytz
import time as time_right_now
import sentiment
import manage_data
import alpaca_trade_api as trade_api
import time as t

stocks_list = ['TSLA', 'GOOGL', 'AAPL', 'MSFT', 'BABA']
stock_dict = {}
columns = ['Date', 'Time', 'Price', '50-Day MA', '200-Day MA', 'Market Open', 'Prev Close', 'Trading Volume', 'Sentiment', 'Subjectivity']
for stock in stocks_list:
    stock_dict[stock] = pd.DataFrame(columns = columns)

base_url = 'https://finance.yahoo.com/quote/'
rest_of_url = '?p='

def scrape(stocks = stocks_list, dictionary = stock_dict):
    key_id = "PKBOHP3XJ2CGC13FQ9Y0"
    secret_key = "d0O/vHoP2yQSzEBpszuVEplLMypcPLDmKe77KNTL"

    api = trade_api.REST(key_id, secret_key)
    clock = api.get_clock()

    while(clock.is_open):
        for ticker in stocks_list:
            url = base_url + ticker + rest_of_url + ticker
            r = requests.get(url)
            soup = bs4.BeautifulSoup(r.text, 'lxml')
            # print(ticker + ": " + url)

            key_stats_url = base_url + ticker + '/key-statistics' + rest_of_url + ticker
            key_stats_req = requests.get(key_stats_url)
            stats_soup = bs4.BeautifulSoup(key_stats_req.text, 'lxml')

            # date/time
            now = datetime.datetime.now(pytz.timezone('US/Central'))
            date = now.strftime("%b %d, %Y")
            time = now.strftime("%H:%M")

            # price
            price = get_data.get_price(soup)

            # Moving Averages
            fifty_day_SMA = get_data.get_50_SMA(stats_soup)
            t_hundred_day_SMA = get_data.get_200_SMA(stats_soup) 

            # market open/close
            m_open = get_data.get_open(soup)
            p_close = get_data.get_close(soup) 

            # volume
            volume = get_data.get_vol(soup) 
            print(volume)

            # sentiment
            analyze = sentiment.Analysis(ticker);
            sent, subj = analyze.run()

            # append info
            entry = [date, time, price, fifty_day_SMA, t_hundred_day_SMA, m_open, p_close, volume, float(sent), float(subj)]
            stock_dict[ticker] = stock_dict[ticker].append(pd.Series(entry, index=columns), ignore_index=True)
        manage_data.manage_csv(dictionary)
        t.sleep(60)

def display_information(stocks = stocks_list, dictionary = stock_dict):
    for ticker in stocks_list:
        print(ticker + ": ")
        pd.options.display.max_columns = 13
        print(stock_dict[ticker])
        print("*" * 60)
        print("*" * 60, '\n')

