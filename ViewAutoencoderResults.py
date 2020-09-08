from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from Autoencoder import Encoder, Decoder
from Config import *


X_train = []
for i in range(1):
    with os.scandir(SPLIT_IMAGES_PATH + str(i+1) + "/") as entries:
        for entry in entries:
            X_train.append(np.asarray(Image.open(SPLIT_IMAGES_PATH + str(i+1) + "/" + entry.name)))
            if X_train.__len__() == 10:
                break

X_train = np.asarray(X_train)
encoder = Encoder()
decoder = Decoder()

encode_data = encoder.get_predict(X_train)
decode_data = decoder.get_predict(encode_data)


n = 10
plt.figure(figsize=(200, 200))
for i in range(1, n):
    # display original
    ax = plt.subplot(2, n, i)
    plt.imshow(X_train[i])
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + n)
    plt.imshow(decode_data[i])
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()


