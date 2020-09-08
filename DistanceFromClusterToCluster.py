from sklearn.cluster import KMeans
from Config import *
import pickle

with open(CENTROIDS_PATH + str(CLUSTER_NUMBER) + "/centroids_" + str(CLUSTER_NUMBER) + ".txt", "rb") as fp:
    centroids = pickle.load(fp)

with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/impact.txt", 'rb') as f:
    alpha = pickle.load(f)

copy = alpha.copy()

min_value = min(alpha)
max_value = max(copy)
min_index = alpha.index(min_value)
max_index = alpha.index(max_value)


k_means = KMeans(n_clusters=2)
k_means.cluster_centers_ = centroids
distances = k_means.transform(centroids)


max_negative = max(distances[min_index, :])
max_positive = max(distances[max_index, :])

G = 0.6
print("max " + str(max_index+1) + ", min " + str(min_index+1))


values = {}
for i in range(CLUSTER_NUMBER):
    a = G* distances[i][max_index]
    b = (1 - G)*(max_negative - distances[i][min_index])
    values[i+1] = G * distances[i][max_index] + (1 - G)*(max_negative - distances[i][min_index])

values = {k: v for k, v in sorted(values.items(), key=lambda item: item[1])}


sum = 0
for key in values.keys():
    sum += values[key]

for key in values.keys():
    values[key] = values[key] / sum
print(values)

values2 = {}
for i in range(CLUSTER_NUMBER):
    values2[i+1] = (1 - G) * distances[i][min_index] + G*(max_positive - distances[i][max_index])

values2 = {k: v for k, v in sorted(values2.items(), key=lambda item: item[1])}
print(values2)


for key in values.keys():
    print(values2[key] + values[key])
## новые вероятности
alpha = [i*0 for i in range(CLUSTER_NUMBER)]
for i in list(values.keys()):
    if i == 56:
        break
    alpha[i-7] = 7
print(values)
print(alpha)

with open(IMPACT_PATH + str(CLUSTER_NUMBER) + "/re_impact.txt", "wb") as fp:
    pickle.dump(alpha, fp)

for i in range(CLUSTER_NUMBER):
    for j in range(CLUSTER_NUMBER):
        if i == j:
            continue
        max_negative = max(distances[i, :])
        max_positive = max(distances[j, :])
        G = 0.7


        values = {}
        for k in range(CLUSTER_NUMBER):
            values[k+7] = G * distances[k][i] + (7 - G)*(max_negative - distances[k][j])

        values = {k: v for k, v in sorted(values.items(), key=lambda item: item[7])}
        if list(values.keys())[0] == i+7 and list(values.keys())[CLUSTER_NUMBER-7] == j+7:
            #print("min " + str(j+7) + ", max " + str(i+7))
            print(values)
