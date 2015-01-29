#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ASUS-PC
#
# Created:     22/09/2014
# Copyright:   (c) ASUS-PC 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import usrobj as upp
from datetime import datetime

import preprocessor as pp
from recommender import Recommender

def evaluate_accuracy(tdata):
    """
    input the classifier, with test data, return accuracy
    testX is a sparse data, testy is an iterable
    """
    traindata,testinput,expected = testpreprocess(tdata)
    rc = Recommender(traindata)
    recommendations = [rc.recommend(i,number=3) for i in testinput]
    totalhit = 0
    errorlog = []
    for idx,val in enumerate(expected):
        if val in recommendations[idx]:
            totalhit += 1
        else:
            errorlog.append([testinput[idx],recommendations[idx],val])
    
    errorlog = pd.DataFrame(data = errorlog, columns = ['Users','ErrResults','ExpResults'])
    errorlog.to_csv('error'+str(datetime.now())+'.csv')
    return totalhit/len(testinput)

def testpreprocess(testdata):
    '''
    this function will preprocess a np array so that it produces 3 objects
    a) training data
    b) test data
    c) 
    '''
    def sparseMatrixIterator(x):
        cx = x.tocoo()
        for i,j in zip(cx.row,cx.col):
            yield (i,j)
    
    testupp = upp.UserProdPreference.initFromNumpyArray(testdata)
    r = 0
    expectedoutput = []
    testinput = []
    
    for row,col in sparseMatrixIterator(testupp.spdata):
        if row==r:
            testupp.spdata[row,col]=0
            r+=1
            expectedoutput.append(col)
            testinput.append(row)
    
    testinput = [testupp.users[code] for code in testinput]
    expectedoutput = [testupp.prods[code] for code in expectedoutput]
    
    return testupp,testinput,expectedoutput