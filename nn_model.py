import os
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers.core import Dense


class LyricsNN:
    def __init__(self, depth, identifier):
        self.model = Sequential()
        self.identifier = identifier
        self.model_filename = f'models/{self.identifier}.model'
        self.model.add(LSTM(4, input_shape=(2, 2), return_sequences=True))
        for i in range(depth):
            self.model.add(LSTM(8, return_sequences=True))
        self.model.add(LSTM(2, return_sequences=True))
        self.model.summary()
        self.model.compile(optimizer='rmsprop',
                           loss='mse')

    def load_model(self):
        if self.model_filename in os.listdir("."):
            self.model.load_weights(self.model_filename)

    def train(self, x_data, y_data):
        self.model.fit(np.array(x_data), np.array(y_data),
                       batch_size=2,
                       epochs=3,
                       verbose=1)
        self.model.save_weights(self.model_filename)
