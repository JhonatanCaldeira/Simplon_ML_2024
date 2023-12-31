import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from components.data_sc import data_load

import joblib

import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

ML_DIR = os.path.join(PARENT_DIR,'ML')
ENCODER_FILENAME = 'encoder.sav'
ENCODER_FILEPATH = os.path.join(ML_DIR, ENCODER_FILENAME)

MODEL_FILENAME = 'model.sav'
MODEL_FILEPATH = os.path.join(ML_DIR, MODEL_FILENAME)

DATA_DIR = os.path.join(PARENT_DIR,'data')
DATA_FILE = os.path.join(DATA_DIR, 'titanic_out.csv')

"""
Function to serializer one object using joblib method
"""
def joblib_serializer(object, filepath):
    joblib.dump(object, filepath)

"""
Function to unserializer one object using joblib method
"""
def joblib_deserializer(filepath):
    return joblib.load(filepath)

"""
Preprocessing function that encode a DataFrame using get_dummies methode
"""
def preprocessing_model(df: pd.DataFrame):
    columns = ["pclass","sex","sibsp","parch", "embarked"]

    for column in columns:
        df = pd.get_dummies(df, columns=[column],dtype=int)

    joblib_serializer(df, ENCODER_FILEPATH)

"""
Function that creates a DataFrame from a serialized encoder and return its
X_train, X_teste, y_train and y_test
"""
def train_test():
    df = joblib_deserializer(ENCODER_FILEPATH)

    X = df.drop(columns=["survived"], axis=1)
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                         train_size=42)
    
    return X, y, X_train, X_test, y_train, y_test

"""
Apply SVM over the titanic data, recovered from the serialized encoder.
Return a serialized model
"""
def svc_model():

    X, y, X_train, X_test, y_train, y_test = train_test()
    
    sc = StandardScaler()
    X = sc.fit_transform(X)
    X_train.iloc[:,:2] = sc.fit_transform(X_train.iloc[:,:2])

    classifier = SVC(kernel='rbf')
    classifier.fit(X_train, y_train)

    joblib_serializer(classifier, MODEL_FILEPATH)

"""
Evaluate the Score from a serialized model.
"""
def model_score():
    X, y, X_train, X_test, y_train, y_test = train_test()

    sc = StandardScaler()
    X = sc.fit_transform(X)
    X_train.iloc[:,:2] = sc.fit_transform(X_train.iloc[:,:2])
    X_test.iloc[:,:2] = sc.transform(X_test.iloc[:,:2])
    
    classifier = joblib_deserializer(MODEL_FILEPATH)

    result = classifier.score(X_test,y_test)
    return result

if __name__ == '__main__':
    df_titanic = data_load(DATA_FILE)
    preprocessing_model(df_titanic)
    svc_model()