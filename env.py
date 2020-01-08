# https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
# ^^ full github to above: https://github.com/notadamking/Stock-Trading-Environment
# https://github.com/llSourcell/Q-Learning-for-Trading/blob/master/envs.py

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

        #merge csv's and rename the rows
        main_list = []
        for stock in stocks_list: # Join all stocks df into single df
            dataFrame_list[stock] = replaceZeros(dataFrame_list[stock])
            dataFrame_list[stock].rename(columns={'Price': f"{stock}_Price",'50-Day MA': f"{stock}_50-Day MA", \
                                            '200-Day MA': f"{stock}_200-Day MA",\
                                            'Market Open': f"{stock}_Market Open",'Prev Close': f"{stock}_Prev Close",\
                                            'Trading Volume': f"{stock}_Trading Volume",'Sentiment': f"{stock}_Sentiment",\
                                            'Subjectivity': f"{stock}_Subjectivity",}, inplace=True)
            if len(main_list)==0:  # If dataframe is empty
                #main_df = dataFrame_list[stock]  # then it's just the current df
                main_list.append(dataFrame_list[stock])
                n_columns = len(dataFrame_list[stock].columns) - 2 # dont include date/time
            else:  # otherwise, join this data to the main one
                dataFrame_list[stock].drop(columns=['Date', 'Time'], inplace=True) # Delete the date/time if it is not the first stock b/c repeats
                main_list.append(dataFrame_list[stock])
        main_df = pd.concat(main_list,axis=1)
        main_df.dropna(inplace=True) #drop nan values
        
        self.stocks_list = stocks_list
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        self.n_stocks = len(stocks_list)
        self.main_df = self.normalizeBetweenZeroAndOne(main_df)
        self.current_step = 0
        #self.n_observes = 2*60*24 # not including current observe (must add one)
        self.OHLC_ect = n_columns  # Open high low close, sentiment ect...
        self.shared_vals = 4 # balance, net worth, date, time
        self.unshared_vals = 4 # shares held, cost basis, ect...
        self.isATest = isATest # Boolean: call alpaca or do not call alpaca
        self.choices = 2 # buy sell
        self.percentOptions = 4 # .25, .5, .75, 1
        
        # Action space: one hot encoding. choose 1 stock out of n+1 to buy/sell and choose % .25, .5, .75, 1
        # the n+1 option is to choose no stock and effectively hold.
        self.acctions = (self.n_stocks+1)*self.choices*self.percentOptions
        self.action_space = spaces.Box(low=0, high=1, shape=(self.acctions,), dtype=np.int64)
        # Observations are ohlc ect as percentages for n observations and n stocks. also shared/unshared values.
        self.obbserves = self.shared_vals+(self.OHLC_ect+self.unshared_vals)*self.n_stocks
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.obbserves,),
                                        dtype=np.float16) # Need to change shape because basic values are diff for diff stocks
    def _next_observation(self):
        obs = list(self.main_df.iloc[self.current_step, :])
        # data shared by all stocks)
        obs.append(self.balance / MAX_ACCOUNT_BALANCE)
        obs.append(self.max_net_worth / MAX_ACCOUNT_BALANCE)
        # data tied to a given stock and not shared by all stocks
        for i, stock in enumerate(self.stocks_list):
            obs.append(self.shares_held[i] / MAX_NUM_SHARES)
            obs.append(self.cost_basis[i] / MAX_SHARE_PRICE)
            obs.append(self.total_shares_sold[i] / MAX_NUM_SHARES)
            obs.append(self.total_sales_value[i] / (MAX_NUM_SHARES * MAX_SHARE_PRICE))
        return np.array(obs)
    def dateToFloat(self, day):
        toReturn = ""
        monthDict = {
            'Jan':'1',
            'Feb':'2',
            'Mar':'3',
            'Apr':'4',
            'May':'5',
            'June':'6',
            'July':'7',
            'Aug': '8',
            'Sept':'9',
            'Oct':'10',
            'Nov' :'11',
            'Dec':'12'
        }
        listDay = day.split()
        listDay[0] = monthDict[listDay[0]]
        listDay[1] = listDay[1].replace(",", "")
        toReturn = float(listDay[0] + listDay[1] + listDay[2])
        #split into an array to deal with month, day year separately
        return toReturn
    def normalizeBetweenZeroAndOne(self, main_df):
        # update date
        dates = main_df['Date'].values
        main_df['Date'] = [float(self.dateToFloat(day)/MAX_TIME) for day in dates] # get dates w/out spaces as floats; divided by max date
        # update time
        time = main_df['Time'].values
        main_df['Time'] = [float(t[0:2] + t[3:])/MAX_DATE for t in time] #delete colon and div by max time
        #amounts like price
        amountsLikePrice = ["Price", "50-Day MA", '200-Day MA', 'Market Open', 'Prev Close'] #can divide by max share price
        for stock in self.stocks_list:
            for amount in amountsLikePrice:
                column = stock + "_" + amount
                likePriceList = main_df[column].values
                main_df[column] = [p/MAX_SHARE_PRICE for p in likePriceList]
            #volume
            volList = main_df[stock + "_" + 'Trading Volume']
            main_df[stock + "_" + 'Trading Volume'] = [v/MAX_VOLUME for v in volList]
        #other columns already between 0 and 1
        return main_df
    def _take_action(self, action): # Buy Sell ect..
        # n_stocks+1 (stocks plus hold) sets of 8 elements
        # of the 8 elements, 1st 4 indicate a buy, second 4 indicate a sell
        # within each set of 4: 1 is 25%, 2 is 50%, .. 1 is 100%
        
        indice = action    
        print('action' + str(indice))
        # find percent by mod 4 plus 1
        percent = int(indice % self.percentOptions) + 1 # 1 is 25%.. 4 is 100%
        print('percent' + str(percent))
        # find buy sell by dividing by 4 (round down)
        buySell = indice % (self.percentOptions * self.choices) #0 thru 3 is buy 4 thru 7 is sell
        print('buySell' + str(buySell))
        # find stock by dividing by 8
        stock_index = int(int(indice) / int(self.percentOptions * self.choices)) # starts at zero indice.
        
        if stock_index == self.n_stocks:
            return # indice n_stocks indicates a hold
        if buySell < 4: 
            self.buy(float(percent)*.25, self.stocks_list[stock_index], stock_index)
        else:
            self.sell(float(percent)*.25, self.stocks_list[stock_index], stock_index)

    def buy(self, n_percent, stock, i):
        print("inside buy")
        row = self.current_step
        column = stock + "_Price"
        price = self.main_df[column].tolist()[row] * MAX_SHARE_PRICE # we normalized it for the neural net.
        
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
        print("inside sell")
        row = self.current_step
        column = stock + "_Price"
        price = self.main_df[column].tolist()[row] * MAX_SHARE_PRICE # we normalized it for the neural net.
        if self.isATest:
            # Sell amount % of shares held
            shares_sold = int(self.shares_held[i] * n_percent) # do not divide by n stocks be because it is for a specific stock
            self.balance += shares_sold * price
            self.shares_held[i] -= shares_sold
            self.total_shares_sold[i] += shares_sold
            self.total_sales_value[i] += shares_sold * price
        else:
            #use alpaca
            blah = "blah"

    def step(self, action):
        # Execute one time step within the environment

        self._take_action(action) 

        self.current_step = self.current_step + 1

        if self.current_step > (len(self.main_df.index) - 1):
            self.current_step = 0

        delay_modifier = (self.current_step / MAX_STEPS)

        reward = self.balance 
        for i, stock in enumerate(stocks_list):
            reward = reward + self.total_sales_value[i]
        reward = reward * delay_modifier
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
            0, len(self.main_df.index) - 1)

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
            
        #print(f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
        print(f'Profit: {profit}')
