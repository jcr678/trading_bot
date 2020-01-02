import gym
from gym import spaces
import random
import json
import pandas as pd
import numpy as np

MAX_ACCOUNT_BALANCE = 2147483647
MAX_NUM_SHARES = 2147483647
MAX_SHARE_PRICE = 5000
MAX_OPEN_POSITIONS = 5
MAX_STEPS = 20000

INITIAL_ACCOUNT_BALANCE = 10000
# https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
# ^^ full github to above: https://github.com/notadamking/Stock-Trading-Environment
# https://github.com/llSourcell/Q-Learning-for-Trading/blob/master/envs.py


class CustomEnv(gym.Env):
  __init__(self, dataFrame_list, stocks_list): # order of df list and stocks list MUST be same!!!!!!!!
    super(CustomEnv, self).__init__()

    main_df = pd.DataFrame()
    for stock in stocks_list: # Join all stocks df into single df
      dataFrame_list[stock].rename(columns={'Date': f"{stock}_Date", "Time": f"{stock}_Time" \\
                                            'Price': f"{stock}_Price",'50-Day MA': f"{stock}_50-Day MA",\\
                                            '200-Day MA': f"{stock}_200-Day MA",'Market Open': f"{stock}_Market Open",\\
                                            'Market Open': f"{stock}_Market Open",'Prev Close': f"{stock}_Prev Close",\\
                                            'Trading Volume': f"{stock}_Trading Volume",'Sentiment': f"{stock}_Sentiment",\\
                                            'Subjectivity': f"{stock}_Subjectivity",}, inplace=True)
      if len(main_df)==0:  # If dataframe is empty
          main_df = dataFrame_list[stock]  # then it's just the current df
          columns = dataFrame_list[stock].columns
      else:  # otherwise, join this data to the main one
          main_df = main_df.join(dataFrame_list[stock])

    self.stocks_list = stocks_list
    self.reward_range = (0, MAX_ACCOUNT_BALANCE)
    self.n_stocks = len(stocks_list)
    self.dataFrame = main_df
    self.cur_step = 0
    self.n_observes = 6 # Inclusive of current observe
    self.OHLC_ect = columns  # Open high low close, sentiment ect...
    self.basic_values
    
    # Action space: discrete # of action types (buy, sell, and hold) &
    # continuous spectrum of amounts to buy/sell (0-100% of account/n_stocks).
    # Actions are 0,1,2 and percent for n stocks
    self.action_space = spaces.Box(low=np.array([0, 0]*self.n_stocks), high=np.array([3, 1]*self.n_stocks), dtype=np.float16)
    # Observations are ohlc ect as percentages for n observations and n stocks
    self.observation_space = spaces.Box(low=0, high=1, shape=(((self.+1)*self.OHLC_ect*self.n_stocks+self.basic_values,)),
                                        dtype=np.float16)
  def _next_observation(self):
    frame = []
    for stock in self.stocks_list:
        f = np.array([[ #assuming normalized
                    df.loc[self.current_step - self.n_observes: self.current_step,
                           f"{stock}_Date"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Time"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Price"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_50-Day MA"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_200-Day MA"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Market Open"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Prev Close"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Trading Volume"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Sentiment"].values,
                    df.loc[self.current_step - self.n_observes: self.current_step, f"{stock}_Subjectivity"].values
                ]])

        frame = np.append(frame, f)
                    # Append additional data and scale each value to between 0-1
    obs = np.append(frame, [ # has length of basic values
                balance / MAX_ACCOUNT_BALANCE,
                max_net_worth / MAX_ACCOUNT_BALANCE,
                shares_held / MAX_NUM_SHARES,
                cost_basis / MAX_SHARE_PRICE,
                total_shares_sold / MAX_NUM_SHARES,
                total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),
            ], axis=0)
    return obs
     
  def _take_action(self, action): # Buy Sell ect..
    pass
  def _step(self, action):
    # Execute 1 time step within the environment
    self._take_action(action)
    self.current_step += 1

    # Do other stuff
    return obs, reward, done, {}
  def reset(self):# Reset the state of the environment to an initial state
    self.cur_step = 0
    # Do other stuff
  def render(self, mode='human', close=False):# Print stuff to console
    pass
