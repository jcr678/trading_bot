import tensorflow as tf
from tensorflow.keras import layers

class MachineLearningModel:
    def __init__(self, input_size):
        # 30 days of input, size won't be 30 though, this should be changed:
        #we could have a counter in the loop that says how much data collected
        self.input_size = 30
        # buy, sell, hold
        self.actions = 3
        self.initializier = 'random_uniform'
        self.activation = 'relu'
        self.loss = "mean_squared_logarithmic_error"
        self.optimizer = keras.optimizers.SGD(learning_rate=0.01, momentum=0.0, nesterov=False)
    def build_mode(self):
        model = Sequential()
        model.add(LSTM(units = 32, input_dim = self.input_size, kernel_initializer = self.initializer))
        model.add(Activation(self.activation))

        model.add(Dropout(rate = .02))

        moodel.add(Dense(units = 64, kernel_initalizer = self.initializer))
        model.add(Activation(self.activation))

        model.add(Dense(units = 16, kernel_initializer = self.initializer))
        model.add(Activation = self.activation)

        model.add(Dense(units = self.actions, kernel_initializer = self.initializer))

        model.compile(loss = self.loss, optimizer = self.optimiizer)
        return model

    def train_model(self, listOfPandasDatabases):
    #make tensorflow model
        # listOfPandasDatabaes[Data and time columns] = X.vectors
        # listOfPandasDatabaes[all the other columns] = Y.vectors
        # model.fit(x_train, y_train, x_test, y_test) --> i think?
        pass
    def run_model(self, toPredictData):
        # model.pred(x_test)
        pass
    def preprocess_data(self):
    #may be unnecessary dependent on model
    #??normalize all values between 0 and 1??
        pass
