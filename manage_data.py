import pandas as pd
import os
from os import path

def manage_csv(stock_dict):
    for stock in stock_dict:
        cwd = os.getcwd()
        csv_path = cwd + '/stocks/' + stock + '.csv'
        if(not path.exists(csv_path)):
            stock_dict[stock].to_csv(csv_path, index=False)
        else:
            df = pd.read_csv(csv_path)
            frames = [df, stock_dict[stock]]
            new_df = pd.concat(frames, sort=False)
            new_df.to_csv(csv_path, index=False)
            print(new_df.head())


'''
Different Solution:
with open("write.csv","a") as f:
    df.to_csv(f,header=False,index=False)
'''
