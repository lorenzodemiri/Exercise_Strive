import numpy as np
from numpy.core.defchararray import greater
from sklearn.preprocessing import StandardScaler
class LinearRegression_scratch():

    def __init__(self, learning_rate = 0.1, iterations = 1000, norm = False):
        self.learing_rate = learning_rate
        self.iteration = iterations
        self.normalize = norm
    
    def fit(self, X_train, y_train):
        # number of the training sample, number of features
        self.m, self.n = X_train.shape
        #Initialize the coefficient at 0
        self.Weights = np.zeros(self.n)
        print(self.Weights)
        self.b = 0
        if self.normalize is False:
            self.X_train = X_train
            self.y_train = y_train
        else: 
            scaler = StandardScaler()
            scaler.fit(X_train)
            self.X_train = scaler.transform(X_train)
            self.y_train = y_train
        #Start iterating and optimizing the coefficient 
        for i in range(self.iteration):
            self.get_updated_weights()

        return self

    def get_updated_weights(self):
        #Initialize the latest status of our linear model
        y_pred = self.predict(self.X_train)
        #Derivate and optimize the Coefficients
        dW = - ((2 * np.dot(self.X_train.T ,self.y_train - y_pred) ) / self.m)
        db = - (2 * np.sum(self.y_train - y_pred) / self.m)
        #Update the global value of the coefficient 
        self.Weights = self.Weights - (self.learing_rate * dW)
        self.b = self.b - (self.learing_rate * db)
        self.learing_rate = self.learing_rate/ 1.05
        return self

    def predict(self, X_train):
        return np.dot(X_train ,self.Weights) + self.b



    

    def coef_(self):
        #Return us the coeficcient of the Linear Model
        return self.Weights, self.b
    
    def score(X_pred, y_test):
        #R-squared that gives us the regression metric
        ss_total = np.sum((y_test - np.mean(y_test)) ** 2)
        ss_res = np.sum((y_test - X_pred) ** 2)
        return (1 - (ss_res/ss_total))

'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
df = pd.read_csv('./ai-f20-m3/d6_linear_regression/reg_data.csv', header=None)

X = df.iloc[:,:-1].values
y = df.iloc[:,1].values
print(X.shape, y.shape)

#
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size =1/3, random_state = 0 ) 
print(len(X_train.shape))
lineaRgs = LinearRegression_scratch(norm = True)
lineaRgs.fit(X_train, Y_train)
lineaRgs.predict(X_test)
print(np.round(lineaRgs.predict(X_test)[:3], 2))
plt.scatter(lineaRgs.predict(X_train),lineaRgs.predict(X_train) - Y_train)
plt.show()

'''
        

