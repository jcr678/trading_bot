import scrape
import models
import sentiment
import pandas as pd
from env import CustomEnv

def main():
    scrape.scrape()
    # scrape.display_information()


if __name__ == "__main__":
    #main()
    #get the csv files as dicts
    stocks_list = ['TSLA', 'GOOGL', 'AAPL', 'MSFT', 'BABA']
    stock_dict = {}
    for stock in stocks_list:
        stock_dict[stock] = pd.read_csv(stock + '.csv')
    #pass to env
    env = CustomEnv(stock_dict, stocks_list, True)
