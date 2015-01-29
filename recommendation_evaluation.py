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
import preprocessor as pp
from recommender import Recommender

def evaluate_accuracy(tdata):
    """
    input the classifier, with test data, return accuracy
    testX is a sparse data, testy is an iterable
    """
    testX,testy,users = testpreprocess(tdata)
    rc = Recommender(testX)
    recommendations = [rc.recommend(i,number=3) for i in users]
    totalhit = 0
    for idx,val in enumerate(testy):
        if val in recommendations[idx]:
            totalhit += 1
        
    return totalhit/len(testy)

def testpreprocess(testdata):
    cusid = testdata['CustomerID']
    testdf = pd.DataFrame(testdata).groupby(['CustomerID','ProductCode']).sum()
    
    testX,testy = [],[]    
    for c in cusid:
        testX = testdf.xs(c).ix[1:]
        testy = testdf.xs(c).ix[:1]
    
    testXdf = pd.concat(testX)
    testydf = pd.concat(testy).values
    
    tdata = testXdf.reset_index().values
    testspmat,m1,m2 = pp.convert3DlistToMatrix(tdata,'CustomerID','ProductCode','Quantity')
    return testspmat,testydf,m1
    pass