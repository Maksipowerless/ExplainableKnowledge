import os
from PIL import Image
import numpy as np
import pickle
from Config import *

Image.MAX_IMAGE_PIXELS = None  # позволяет окрывать изображения большого размера

positive = []
negative = []
for i in range(CLUSTER_NUMBER):
    positive.append(0)
    negative.append(0)
mask_list = [4, 9, 10]

for i in mask_list:

    centroids = []
    with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + '/' + str(i) + '.txt', 'rb') as f:
        centroids = pickle.load(f)

    mask = Image.open(MASK_PATH + str(i) + ".tif")
    mask_array = np.array(mask).copy()

    PATH_SPLIT_IMAGES = './images/split_images/' + str(i) + "/"
    entries = sorted(os.scandir(PATH_SPLIT_IMAGES), key=lambda x: (x.is_dir(), x.name))
    count = 0
    for entry in entries:
        tmp = entry.name.split('.')
        tmp = tmp[0]
        tmp = tmp.split('_')
        column = int(tmp[0])
        row = int(tmp[1])
        current_centroid = centroids[count]

        a = mask_array[128*(column-1):128*column, 128*(row-1):128*row, :]
        unique, counts = np.unique(a, return_counts=True)

        if 0 in unique:
            positive[current_centroid - 1] +=1
        else:
            negative[current_centroid - 1] +=1
        count += 1

old_negative = []
old_positive = []
with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/negative_cluster.txt", 'rb') as f:
    old_negative = pickle.load(f)
with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/positive_cluster.txt", 'rb') as f:
    old_positive = pickle.load(f)

n = [old_negative[i] + old_positive[i] for i in range(CLUSTER_NUMBER)]
alpha = []
with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/impact.txt", 'rb') as f:
    alpha = pickle.load(f)


re_impact = []
for i in range(CLUSTER_NUMBER):
    value = (n[i]*alpha[i] + positive[i]) / (n[i] + positive[i] + negative[i])
    re_impact.append(value)

print(re_impact)
with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/re_impact.txt", "wb") as fp:
    pickle.dump(re_impact, fp)

