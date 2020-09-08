from keras.layers import Input, Dense, Conv2D, Concatenate, Dropout, Flatten, Reshape, UpSampling2D
from keras.models import Model
import numpy as np
from Config import *


class Encoder:

    def __init__(self):
        input_img = Input(shape=(128, 128, 3))
        conv2d_1 = Conv2D(6, (5, 5), activation='relu', padding='same')(input_img)
        conv2d_2 = Conv2D(6, (5, 5), activation='relu', padding='same')(input_img)
        conv2d_3 = Conv2D(12, (5, 5), activation='relu', padding='same')(conv2d_2)
        conv2d_4 = Conv2D(6, (5, 5), activation='relu', padding='same')(input_img)
        conv2d_5 = Conv2D(12, (5, 5), activation='relu', padding='same')(conv2d_4)
        conv2d_6 = Conv2D(24, (5, 5), activation='relu', padding='same')(conv2d_5)
        merge_1 = Concatenate()([input_img, conv2d_1, conv2d_3, conv2d_6])
        conv2d_7 = Conv2D(32, (5, 5), activation='relu', padding='same')(merge_1)
        conv2d_8 = Conv2D(32, (5, 5), strides=4, activation='relu', padding='same')(conv2d_7)
        dropout_1 = Dropout(0.0)(conv2d_8)
        conv2d_9 = Conv2D(32, (5, 5), strides=4, activation='relu', padding='same')(dropout_1)
        dropout_2 = Dropout(0.0)(conv2d_9)
        flatten_1 = Flatten()(dropout_2)
        dense_1 = Dense(2048)(flatten_1)
        intermediate_layer = Dropout(0.0)(dense_1)
        self.__encoder = Model(input_img, intermediate_layer, name='encoder')
        self.__encoder.load_weights(AUTOENCODER_WEIGHTS_PATH + "encoder_weights")

    def get_predict(self, data):
        return np.asarray(self.__encoder.predict(data))


class Decoder:

    def __init__(self):
        bottle_neck = Input(shape=(2048,))
        reshape_1 = Reshape((8, 8, 32))(bottle_neck)
        up_sampling2d_1 = UpSampling2D((4, 4))(reshape_1)
        conv2d_10 = Conv2D(32, (5, 5), activation='relu', padding='same')(up_sampling2d_1)
        up_sampling2d_2 = UpSampling2D((4, 4))(conv2d_10)
        conv2d_11 = Conv2D(45, (5, 5), activation='relu', padding='same')(up_sampling2d_2)
        conv2d_12 = Conv2D(3, (5, 5), activation='relu', padding='same')(conv2d_11)
        self.__decoder = Model(bottle_neck, conv2d_12, name='decoder')
        self.__decoder.load_weights(AUTOENCODER_WEIGHTS_PATH + "decoder_weights")

    def get_predict(self, data):
        return np.asarray(self.__decoder.predict(data), dtype=int)


