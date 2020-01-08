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
    env.reset()
    envShape = env._next_observation().shape[0]
    agent = ActorCriticAgent(env.acctions, env.obbserves)
    
    num_episodes = 2000
    for i in range(num_episodes):
        done = False
        observation = env.reset()
        i = 0
        while not done:
            if (i % 100) == 1:
                env.render()
            i = i + 1
            action = agent.choose_action(observation)
            observation_, reward, done, _ = env.step(action)
            agent.learn(observation, action, reward, observation_, done)
            observation = observation_
    
