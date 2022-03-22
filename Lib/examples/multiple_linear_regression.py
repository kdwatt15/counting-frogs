# tutorial from https://www.machinelearningworks.com/tutorials/multiple-linear-regression

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import os

# load data
dataset = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data','50_Startups.csv'))

x = dataset.iloc[:, 0:4].values
y = dataset.iloc[:, -1].values

# data preprocessing
encoder = OneHotEncoder(drop="first", dtype=int)
ct = ColumnTransformer([('categorical_encoding', encoder, [3])], remainder="passthrough")

x = ct.fit_transform(x)

# creating test and training datasets
def create_test_data(x, y, random_state=0):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.25, random_state=random_state)
    return x_train, x_test, y_train, y_test

# train and evaluate the performance of the model
def train_dataset(random_state):
    x_train, x_test, y_train, y_test = create_test_data(x, y)
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)

    predictions = regressor.predict(x_test)
    r_squared = r2_score(y_test, predictions)

    n = len(x_test)
    k = 5
    adjusted_r_squared = 1 - (((1 - (r_squared ** 2)) * (n - 1)) / (n - k - 1))
    print(f'The adjusted R score of the model is: {adjusted_r_squared}')

    return {
        "x_train": x_train,
        "y_train": y_train,
        "x_test": x_test,
        "y_test": y_test,
        "adjusted_r_squared": adjusted_r_squared,
        "predictions": predictions,
        "coef": regressor.coef_
    }

if __name__ == '__main__':
    a = train_dataset(random_state=0)