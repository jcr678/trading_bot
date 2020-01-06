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
    print(env._next_observation())

    '''for e in range(n_episodes): # iterate over new episodes of the game
    state = env.reset() # reset state at start of each new episode of the game
    state = np.reshape(state, [1, state_size])
    
    https://github.com/the-deep-learners/TensorFlow-LiveLessons/blob/master/notebooks/cartpole_dqn.ipynb
    
    for time in range(5000):  # time represents a frame of the game; goal is to keep pole upright as long as possible up to range, e.g., 500 or 5000 timesteps
#         env.render()
        action = agent.act(state) # action is either 0 or 1 (move cart left or right); decide on one or other here
        next_state, reward, done, _ = env.step(action) # agent interacts with env, gets feedback; 4 state data points, e.g., pole angle, cart position        
               
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done) # remember the previous timestep's state, actions, reward, etc.        
        state = next_state # set "current state" for upcoming iteration to the current next state        
        if done: # episode ends if agent drops pole or we reach timestep 5000
            print("episode: {}/{}, score: {}, e: {:.2}" # print the episode's score and agent's epsilon
                  .format(e, n_episodes, time, agent.epsilon))
            break # exit loop
    if len(agent.memory) > batch_size:
        agent.replay(batch_size) # train the agent by replaying the experiences of the episode
    if e % 50 == 0:
        agent.save(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")'''
