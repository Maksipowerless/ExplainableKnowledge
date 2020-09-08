import os
from sklearn.cluster import KMeans
from Autoencoder import Encoder
from PIL import Image
import numpy as np
import pickle
from Config import *


class FeatureGeneration:

    def __init__(self):
        self.__encoder = Encoder()
        self.points = []
        self.positive_cluster = [i*0 for i in range(CLUSTER_NUMBER)]
        self.negative_cluster = [i*0 for i in range(CLUSTER_NUMBER)]

    def add_patches(self, list):
        for i in list:
            entries = sorted(os.scandir(SPLIT_IMAGES_PATH + str(i) + "/"), key=lambda x: (x.is_dir(), x.name))
            for entry in entries:
                a = []
                a.append(np.asarray(Image.open(SPLIT_IMAGES_PATH + str(i) + "/" + entry.name)))
                image = np.asarray(a)
                self.points.append(self.__encoder.get_predict(image).reshape(2048))
        self.points = np.asarray(self.points)

    def find_centroids(self, num, list):
        k_means = KMeans(n_clusters=num)
        k_means.fit(self.points)
        centroids = k_means.cluster_centers_
        with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + "/centroids_" + str(num)+".txt", "wb") as fp:
            pickle.dump(centroids, fp)

    def find_patches_score_from_centroids(self, list):
        with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + "/centroids_" + str(CLUSTER_NUMBER)+".txt", "rb") as fp:
            centroids = pickle.load(fp)
        k_means = KMeans(n_clusters=CLUSTER_NUMBER)
        k_means.cluster_centers_ = centroids

        for i in list:
            entries = sorted(os.scandir(SPLIT_IMAGES_PATH + str(i) + "/"), key=lambda x: (x.is_dir(), x.name))
            significant_feature_number = []
            for entry in entries:
                tmp = []
                tmp.append(np.asarray(Image.open(SPLIT_IMAGES_PATH + str(i) + "/" + entry.name)))
                image = np.asarray(tmp)
                bottle_neck = self.__encoder.get_predict(image)
                tmp = k_means.predict(bottle_neck) + 1
                significant_feature_number.append(tmp[0])

            with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + "/" + str(i) + ".txt", "wb") as fp:
                pickle.dump(significant_feature_number, fp)

    def find_patches_score_from_medoids(self, list):
        pass

    def find_impact(self, positive_list, negative_list):
        negative = []
        for i in negative_list:
            with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + '/{}.txt'.format(i), 'rb') as f:
                negative += pickle.load(f)

        n_negative = negative.__len__()
        negative_arr = np.asarray(negative)
        unique, counts = np.unique(negative_arr, return_counts=True)
        negative_dictionary = dict(zip(unique, counts))
        print(negative_dictionary)
        for key in negative_dictionary.keys():
            self.negative_cluster[key-1] = negative_dictionary[key]

        for k in negative_dictionary.keys():
            negative_dictionary[k] = negative_dictionary[k] / n_negative

        positive = []
        for i in positive_list:
            with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + '/{}.txt'.format(i), 'rb') as f:
                positive += pickle.load(f)

        n_positive = positive.__len__()
        positive_arr = np.asarray(positive)
        unique, counts = np.unique(positive_arr, return_counts=True)
        positive_dictionary = dict(zip(unique, counts))
        print(positive_dictionary)
        for key in positive_dictionary.keys():
            self.positive_cluster[key - 1] = positive_dictionary[key]

        for k in positive_dictionary.keys():
            positive_dictionary[k] = (positive_dictionary[k] / n_positive)

        impact = []
        for i in range(CLUSTER_NUMBER):
            if positive_dictionary.keys().__contains__(i + 1) == False:
                impact.append(0)
            elif negative_dictionary.keys().__contains__(i + 1) == False:
                impact.append(1)
            else:
                value = positive_dictionary[i + 1] / (positive_dictionary[i + 1] + negative_dictionary[i + 1])
                impact.append(value)

        with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/impact.txt", "wb") as fp:
            pickle.dump(impact, fp)
        print(impact)

    def save_cluster_capacity(self):
        with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/positive_cluster.txt", "wb") as fp:
            pickle.dump(self.positive_cluster, fp)

        with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/negative_cluster.txt", "wb") as fp:
            pickle.dump(self.negative_cluster, fp)


negative_list = [2, 11, 14, 15, 18, 19, 20]
positive_list = [8, 5, 7, 12, 13, 16, 17]
list = negative_list + negative_list


fg = FeatureGeneration()
fg.add_patches(list)
fg.find_centroids(CLUSTER_NUMBER, list)
fg.find_patches_score_from_centroids(list)
fg.find_impact(positive_list, negative_list)
fg.save_cluster_capacity()