import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from Autoencoder import Encoder
from Config import *
import pickle


with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + "/centroids_" + str(CLUSTER_NUMBER) + ".txt", "rb") as fp:
    centroids = pickle.load(fp)

with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/impact.txt", 'rb') as f:
    alpha = pickle.load(f)

min_value = min(alpha)
max_value = max(alpha)
min_index = alpha.index(min(alpha))
max_index = alpha.index(max(alpha))

centroids_min_max = np.asarray([centroids[min_index], centroids[max_index]])

distance_dict = {}
for i in range(CLUSTER_NUMBER):
    distance_dict[i] = {}


k_means = KMeans(n_clusters=2)
k_means.cluster_centers_ = centroids_min_max
encoder = Encoder()


list = [4, 9, 10, 14, 15, 19]
for i in list:
    with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + "/" + str(i) + ".txt", 'rb') as f:
        patch_clusters = pickle.load(f)
    entries = sorted(os.scandir(SPLIT_IMAGES_PATH + str(i) + "/"), key=lambda x: (x.is_dir(), x.name))
    count = 0
    for entry in entries:
        tmp = []
        tmp.append(np.asarray(Image.open(SPLIT_IMAGES_PATH + str(i) + "/" + entry.name)))
        image = np.asarray(tmp)
        bottle_neck = encoder.get_predict(image)
        tmp = k_means.transform(bottle_neck)
        distance_dict[patch_clusters[count] - 1][str(i) + "_" + entry.name.split(".")[0]] = (tmp[0][0], tmp[0][1])
        count += 1
    print("done" + str(i))

with open("distances.txt", "wb") as fp:
    pickle.dump(distance_dict, fp)

with open("distances.txt", "rb") as fp:
    distances_neg_pos = pickle.load(fp)


dictionary_cancer = {}
negative_distances = {}
positive_distances = {}
max_negative_distance = {}
max_positive_distance = {}

for i in list:
    negative_distances[str(i)] = {}
    positive_distances[str(i)] = {}
    max_negative_distance[str(i)] = {}
    max_positive_distance[str(i)] = {}

for key in negative_distances.keys():
    for i in range(CLUSTER_NUMBER):
        if i != min_index and i != max_index:
            negative_distances[key][i] = []
            positive_distances[key][i] = []

# вычислить максимальное расстояние от патча к "лучшему" позитивному (негативному) кластеру
for cluster_number in distances_neg_pos.keys():
    if cluster_number != min_index and cluster_number != max_index:
        for im_name_key in distances_neg_pos[cluster_number].keys():
            image_num = im_name_key.split("_")[0]

            negative_distances[image_num][cluster_number].append(distances_neg_pos[cluster_number][im_name_key][0])
            positive_distances[image_num][cluster_number].append(distances_neg_pos[cluster_number][im_name_key][1])




GAMMA_LIST = [0.2, 0.4, 0.6, 0.8]
DELTA_LIST = [0.2, 0.4, 0.6, 0.8]

for GAMMA in GAMMA_LIST:
    for DELTA in DELTA_LIST:

        for i in list:
            for j in range(CLUSTER_NUMBER):
                if j != min_index and j != max_index:
                    if negative_distances[str(i)][j].__len__() != 0:
                        max_negative_distance[str(i)][j] = max(negative_distances[str(i)][j])
                        max_positive_distance[str(i)][j] = max(positive_distances[str(i)][j])


        for cluster_number in distances_neg_pos.keys():
            if cluster_number == min_index:
                for im_name_key in distances_neg_pos[cluster_number].keys():
                    dictionary_cancer[im_name_key] = 0

            elif cluster_number == max_index:
                for im_name_key in distances_neg_pos[cluster_number].keys():
                    dictionary_cancer[im_name_key] = 1

            elif alpha[cluster_number] > 0.5:
                distance_dictionary = {}
                for im_name_key in distances_neg_pos[cluster_number].keys():
                    d_neg = distances_neg_pos[cluster_number][im_name_key][0]
                    d_pos = distances_neg_pos[cluster_number][im_name_key][1]
                    distance_dictionary[im_name_key] = GAMMA*d_pos + (1 - GAMMA)*(max_negative_distance[im_name_key.split("_")[0]][cluster_number] - d_neg)
                distance_dictionary = {k: v for k, v in sorted(distance_dictionary.items(), key=lambda item: item[1])}
                patch_count_in_image = len(positive_distances[im_name_key.split("_")[0]][cluster_number])
                cancer_patches_number = int(patch_count_in_image * alpha[cluster_number])
                for key in distance_dictionary.keys():
                    if cancer_patches_number > 0:
                        dictionary_cancer[key] = 1
                    else:
                        dictionary_cancer[key] = 0
                    cancer_patches_number -= 1
            else:
                distance_dictionary = {}
                for im_name_key in distances_neg_pos[cluster_number].keys():
                    d_neg = distances_neg_pos[cluster_number][im_name_key][0]
                    d_pos = distances_neg_pos[cluster_number][im_name_key][1]
                    distance_dictionary[im_name_key] = DELTA * d_neg + (1 - DELTA) * (max_positive_distance[im_name_key.split("_")[0]][cluster_number] - d_pos)
                distance_dictionary = {k: v for k, v in sorted(distance_dictionary.items(), key=lambda item: item[1])}
                patch_count_in_image = len(positive_distances[im_name_key.split("_")[0]][cluster_number])
                non_cancer_patches_number = int(patch_count_in_image * (1 - alpha[cluster_number]))
                for key in distance_dictionary.keys():
                    if non_cancer_patches_number > 0:
                        dictionary_cancer[key] = 0
                    else:
                        dictionary_cancer[key] = 1
                    non_cancer_patches_number -= 1


        images = {}
        for i in list:
            images[str(i)] = {}

        for key in dictionary_cancer.keys():
            new_key = key.split("_")[1] + "_" + key.split("_")[2]
            images[key.split("_")[0]][new_key] = dictionary_cancer[key]

        for key in images.keys():
            with open("./results/im" + key + "_g_" + str(GAMMA) + "_d_" + str(DELTA) + ".txt", "wb") as fp:
                a = images[key]
                pickle.dump(images[key], fp)
