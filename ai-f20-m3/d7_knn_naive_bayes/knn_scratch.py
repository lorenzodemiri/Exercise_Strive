import numpy as np

class KNN:
    def __init__(self, k):
        self.k = k

    def get_euclidean_distance(self, arr1, arr2 ):
        return np.linalg.norm(np.array(arr1) - np.array(arr2))

    def get_k_neighbors(self, arr_test):
        distances = []
        #Calculate distances between each points adding those to distances 
        for i in range(self.n):
            distances.append((self.get_euclidean_distance(arr_test, self.X_train[i]), self.Y_train[i]))
        #Sort the distances
        distances.sort()
        #Take only the first K distances
        return distances[:self.k]

    def get_nearestNeighbor(self):
        neighbors = []
        # Iterate the Test_data to calculate the distance of our X_test points from the X_train points
        for i in range(self.m):
            neighbors.append(self.get_k_neighbors(self.X_test[i]))
        return neighbors

    def target_classificator(self, arr):
        #Dictionary that stores a counter of the neighbors
        ret_dict = {}
        for value in arr:
            if value in ret_dict: ret_dict[value] += 1
            else: ret_dict[value] = 1
        return ret_dict

    def fit(self, X_train, Y_train):
        #Casting the elements to keep data integrety
        self.X_train = np.array(X_train)
        self.Y_train = np.array(Y_train)
        self.n = len(self.X_train)
        return self

    def predict(self, X_test):
        #Casting the elements to keep data integrety
        self.X_test = np.array(X_test)
        self.m = len(self.X_test)
        neighbors = self.get_nearestNeighbor()
        predictions = []
        for value in neighbors:
            dist, labels = zip(*value)
            label_dict = self.target_classificator(labels)
            predictions.append(max(self.target_classificator(labels), key = label_dict.get))
        return predictions

    def score(self, Y_test, Y_pred):
        from sklearn.metrics import accuracy_score
        return accuracy_score(Y_test, Y_pred)

'''
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples=50, centers = 4, cluster_std=0.6, random_state=0)
print(X.shape, y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 1/3, random_state = 0)

knn = KNN(4)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(knn.score(y_pred, y_test))
'''