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

def merge_csvs(lst_csvs = os.listdir('./stocks')):
    df_dict = {}
    for tick in lst_csvs:
        df_dict[tick.split('.csv')[0]] = pd.read_csv('./stocks/' + tick)
    merged = pd.concat(df_dict, axis=1)
    # print(merged.head())
    merged.to_csv('MERGEDSTOCKDATA.csv')
    return merged

# merge_csvs()
'''
Different Solution:
with open("write.csv","a") as f:
    df.to_csv(f,header=False,index=False)
'''
