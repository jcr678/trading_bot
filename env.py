# https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
# ^^ full github to above: https://github.com/notadamking/Stock-Trading-Environment
# https://github.com/llSourcell/Q-Learning-for-Trading/blob/master/envs.py

from replaceZeros import replaceZeros
import gym
from gym import spaces
import random
import pandas as pd
import numpy as np

MAX_VOLUME = 2147483647.0 # Can be changed later to smaller value
MAX_ACCOUNT_BALANCE = 2147483647.0
MAX_NUM_SHARES = 2147483647.0
MAX_SHARE_PRICE = 10000.0
MAX_STEPS = 90000.0 # We need to figure out what this number actually would be... No idea.
MAX_DATE = 12292100.0 # monthDayYear
MAX_TIME = 2400 # 12 at night

INITIAL_ACCOUNT_BALANCE = 10000.0


class CustomEnv(gym.Env):
    def __init__(self, dataFrame_list, stocks_list, isATest): # order of df list and stocks list MUST be same
        super(CustomEnv, self).__init__()

        main_df = pd.DataFrame()
        for stock in stocks_list: # Join all stocks df into single df
            dataFrame_List[stock] = replaceZeros(dataFrame_List[stock]) #get rid of sent/subj zeros
            dataFrame_list[stock].rename(columns={'Price': f"{stock}_Price",'50-Day MA': f"{stock}_50-Day MA", \
                                            '200-Day MA': f"{stock}_200-Day MA",\
                                            'Market Open': f"{stock}_Market Open",'Prev Close': f"{stock}_Prev Close",\
                                            'Trading Volume': f"{stock}_Trading Volume",'Sentiment': f"{stock}_Sentiment",\
                                            'Subjectivity': f"{stock}_Subjectivity",}, inplace=True)
        if len(main_df)==0:  # If dataframe is empty
          main_df = dataFrame_list[stock]  # then it's just the current df
          n_columns = dataFrame_list[stock].columns - 2 # dont include date/time
        else:  # otherwise, join this data to the main one
          dataFrame_list[stock].drop(columns=['Date', 'Time']) # Delete the date/time if it is not the first stock b/c repeats
          main_df = main_df.join(dataFrame_list[stock])

        main_df.dropna(inplace=True) #drop nan values

        self.stocks_list = stocks_list
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        self.n_stocks = len(stocks_list)
        self.main_df = normalizeBetweenZeroAndOne(main_df)
        self.cur_step = 0
        self.n_observes = 2*60*24 # not including current observe (must add one)
        self.OHLC_ect = columns  # Open high low close, sentiment ect...
        self.shared_vals = 2 # balance, net worth
        self.unshared_vals = 4 # shares held, cost basis, ect...
        self.isATest = isATest # Boolean: call alpaca or do not call alpaca

        # Action space: discrete # of action types (buy, sell, and hold) &
        # continuous spectrum of amounts to buy/sell (0-100% of balance/n_stocks or shares_held/n_stocks).
        # Actions are 0,1,2 and percent/n for n stocks
        self.action_space = spaces.Box(low=0, high=1, shape=(self.n_stocks*2,), dtype=np.float16)
        # Observations are ohlc ect as percentages for n observations and n stocks
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.n_observes+1, 
                                                              self.shared_vals+(self.n_columns+self.unshared_vals)*self.n_stocks),
                                        dtype=np.float16) # Need to change shape because basic values are diff for diff stocks
    def _next_observation(self):
        '''
        for stock in self.stocks_list:shape=(((self.n_observes+1)*self.OHLC_ect*self.n_stocks+self.basic_values,)
        f = np.array([[ #assuming normalized between 0 and 1
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
        obs = np.append(frame, [ # has length of basic_values
                balance / MAX_ACCOUNT_BALANCE,
                max_net_worth / MAX_ACCOUNT_BALANCE,
                shares_held / MAX_NUM_SHARES, # Need to update all use list
                cost_basis / MAX_SHARE_PRICE, # "SAME" MAYBE DELETE COST BASIS IDK
                total_shares_sold / MAX_NUM_SHARES, # Need to update all use list
                total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE), # ?Need to update all use list?
            ], axis=0)
        '''
        obs = []
        for i in range(self.current_step - self.n_observes, self.current_step+1):
            # get given row as list
            row = self.main_df.iloc[[i]].tolist()
            # data shared by all stocks)
            row.append(balance / MAX_ACCOUNT_BALANCE)
            row.append(max_net_worth / MAX_ACCOUNT_BALANCE)
            # data tied to a given stock and not shared by all stocks
            for i, stock in self.stocks_list:
                row.append(self.shares_held[i] / MAX_NUM_SHARES)
                row.append(cost_basis[i] / MAX_SHARE_PRICE)
                row.append(total_shares_sold[i] / MAX_NUM_SHARES)
                row.append(total_sales_value[i] / (MAX_NUM_SHARES * MAX_SHARE_PRICE))
                #append the row to the obs
            obs.append(row)
        return obs

    def normalizeBetweenZeroAndOne(main_df):
        # update date
        dates = main_df['Date'].toList()
        main_df['Date'] = [float(day.strip())/MAX_TIME for day in dates] # get dates w/out spaces as floats; divided by max date
        # update time
        time = main_df['Time'].toList()
        main_df['Time'] = [float(t[0:2] + t[3:])/MAX_DATE for t in time] #delete colon and div by max time
        amountsLikePrice = ["Price", "50-Day MA", '200-Day MA', 'Market Open', 'Prev Close'] #can divide by max share price
        for stock in self.stocks_list:
            for amount in amountsLikePrice:
                column = stock + "_" + other
                likePriceList = main_df[column]
                main_df[column] = [p/MAX_SHARE_PRICE for p in likePriceList]
            #volume
            volList = main_df[stock + "_" + 'Trading Volume']
            main_df[stock + "_" + 'Trading Volume'] = [v/MAX_VOLUME for v in volList]
        #other columns already between 0 and 1
        return main_df
        def _take_action(self, action): # Buy Sell ect..
        #use self.isATest to know if u actually buy stocks
            for i, stock in enumerate(self.stocks_list):
                if action[i*2] < 1.0/3.0: # buy
                    buy(self, action[i*2+1], stock, i)
                elif action[i*2] > 2.0/3.0: # sell
                    sell(self, action[i*2+1], stock, i)
                    #hold (do nothing so no statement)

    def buy(self, n_percent, stock, i):
        price = main_df.at(self.step, f"{stock}_Price")
        if self.isATest: #dont use alpaca
            # Buy amount % of balance in shares
            total_possible = int(self.balance / (price * self.n_stocks))
            shares_bought = int(total_possible * n_percent)
            prev_cost = self.cost_basis[i] * self.shares_held[i] # need to turn shares held and cost basis arrays
            additional_cost = shares_bought * price

            self.balance -= additional_cost
            self.cost_basis[i] = (
                prev_cost + additional_cost) / (self.shares_held[i] + shares_bought)
            self.shares_held[i] += shares_bought

        else: #use alpaca
            blah = "blah"
            
    def sell(self, n_percent, stock, i):
        price = main_df.at(self.step, f"{stock}_Price")
        if self.isATest:
            # Sell amount % of shares held
            shares_sold = int(self.shares_held[i] * n_percent/self.n_stocks)
            self.balance += shares_sold * current_price
            self.shares_held[i] -= shares_sold
            self.total_shares_sold[i] += shares_sold
            self.total_sales_value[i] += shares_sold * current_price
        else:
            #use alpaca
            blah = "blah"

    def _step(self, action):
        # Execute one time step within the environment
        self._take_action(action) 

        self.current_step += 1

        if self.current_step > len(main_df.index) - 1:
            self.current_step = 0

        delay_modifier = (self.current_step / MAX_STEPS)

        reward = self.balance * delay_modifier
        done = self.net_worth <= 0

        obs = self._next_observation()

        return obs, reward, done, {}

    def reset(self):# Reset the state of the environment to an initial state
        # Reset the state of the environment to an initial state
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE
        self.shares_held = [0] * self.n_stocks
        self.cost_basis = [0] * self.n_stocks
        self.total_shares_sold = [0] * self.n_stocks
        self.total_sales_value = [0] * self.n_stocks 

        # Set the current step to a random point within the data frame
        self.current_step = random.randint(
            0, len(main_df.index) - 1)

        return self._next_observation()

    def render(self, mode='human', close=False):# Print stuff to console
        
        # Render the environment to the screen
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        
        for i, stock in enumerate(stocks_list):
            print(stock)
            print(f'shares held: {self.shares_held[i]} (Total sold: {self.total_shares_sold[i]})')
            print(f'Avg cost for held shares: {self.cost_basis[i]} (Total sales value: {self.total_sales_value[i]})')
            
        print(f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
        print(f'Profit: {profit}')
