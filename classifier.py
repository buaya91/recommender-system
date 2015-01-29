# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 09:09:29 2014
classify
@author: qingwei
"""
from sklearn.neighbors import KNeighborsClassifier as knn
# import numpy as np

def knnclassify(traindata,trainlabel,target):
    """
    use knn(3) by default
    trainingdata and target has be to numpy array
    """
    model = knn().fit(traindata,trainlabel)
    prediction = model.predict(target)
    
    return prediction
    
def evaluate(traindata,trainlabel,testdata,testlabel):
    model = knn().fit(traindata,trainlabel)
    score = model.score(testdata,testlabel)
    
    return score