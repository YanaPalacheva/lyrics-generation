import os
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers.core import Dense


class LyricsNN:
    def __init__(self, depth, identifier):
        """
        Initialization of LyricsNN class describing an RNN for lines prediction.
        :param depth: number of NN hidden layers, int
        :param identifier: current artist or genre, str
        """
        self.model = Sequential()
        self.identifier = identifier
        self.model_filename = f'models/{self.identifier}.model'
        self.model.add(LSTM(4, input_shape=(2, 2), return_sequences=True))
        for i in range(depth):
            self.model.add(LSTM(8, return_sequences=True))
        self.model.add(LSTM(2, return_sequences=True))
        self.model.compile(optimizer='rmsprop',
                           loss='mse')

    def load_model(self):
        """
        Loading of the trained model from file (stored in 'models' directory).
        """
        if os.path.exists(self.model_filename):
            self.model.load_weights(self.model_filename)

    def train(self, x_data, y_data):
        """
        Training of the model on 2 datasets.
        :param x_data: dataset containing information about odd couplets (syllables and rhyme vectors), np array
        :param y_data: dataset containing information about even couplets (syllables and rhyme vectors), np array
        """
        self.model.fit(np.array(x_data), np.array(y_data),
                       batch_size=2,
                       epochs=3,
                       verbose=1)
        self.model.save_weights(self.model_filename)

    def predict(self, input_vec):
        """
        Prediction function based on an input vector.
        :param input_vec: vector containing information on syllables and rhyme, np array of size (1, 2, 2)
        :return: predicted vector
        """
        return self.model.predict(input_vec)
