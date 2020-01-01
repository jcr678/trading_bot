# code credit goes to https://www.youtube.com/watch?v=2vJtbAha3To&t=956s
from keras import backend as K
from keras.layers import Dense, Input
from keras.models import Model
from keras.optimizers import Adam
import numpy as np

class ActorCriticAgent():
    def __init__(self, n_actions=4, observation_dims=8):
        
        self.gamma = .99 # future reward
        self.alpha = .000001 # alpha and beta are learning rates for 2 neural nets
        self.beta = .00005
        
        self.input_dims = observation_dims
        self.fc1_dims = 1024
        self.fc2_dims = 512
        self.n_actions = n_actions
        
        self.actor, self.critic, self.policy = self.build_actor_critic_network()
        self.action_space = [i for i in range(n_actions)]
        
    def build_actor_critic_network(self): # One network with 2 outputs (reward and action)
        input_ = Input(shape=(self.input_dims, ))
        delta = Input(shape=[1])
        dense1 = Dense(self.fc1_dims, activation='relu')(input_)
        dense2 = Dense(self.fc2_dims, activation='relu')(dense1)
        probs = Dense(self.n_actions, activation='softmax')(dense2) # Pick action
        values = Dense(1, activation='linear')(dense2)# Reward action
        
        def custom_loss(y_true, y_pred):
            out = K.clip(y_pred, 1e-8, 1-1e8) #values cannot be zero or one because we take log
            log_lik = y_true * K.log(out)
            return K.sum(-log_lik*delta)
        actor = Model(input =[input_, delta], output=[probs])
        actor.compile(optimizer=Adam(lr=self.alpha), loss=custom_loss)
        
        critic = Model(input =[input_], output=[values])
        actor.compile(optimizer=Adam(lr=self.beta), loss='mean_squared_error')
                policy = Model(input=[input_], output=[probs])
        
        return actor, critic, policy
    def choose_action(self, observation):
        state=observation[np.newaxis, :]
        probabilities = self.policy.predict(state)[0]
        action = np.random.choice(self.action_space, p=probabilities)
        return action
    def learn(self, state, action, reward, state_, done):
        state = state[np.new_axis, :] # Just add dimention for neural net
        state_ = state_[np.new_axis, :] # Just add dimention for neural net
        
        critic_value_ = self.critic.predict(state_) #future state
        critic_value = self.critic.predict(state) # state
        
        target = reward + self.gamma* critic_value_*(1-int(done)) # stop when done
        delta = target - critic_value 
        
        actions = np.zeros([1, n_self.actions])
        action[np.arange(1)), action] = 1
        
        self.actor.fit([state, delta], actions, verbose=0)
        self.critic.fit(state, target, verbose=0)
    def saveWeights(self):
        pass # Pickle
    def loadWeights(self):
        pass # Pickle
