# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 11:27:45 2014
le main script to run a recommendation service
@author: qingwei
"""
import dataloader as dl
import preprocessor as pp
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
import math
import pandas as pd

def main():
    dataformat = "a10 a10 a10 a10 a10 a10 a10 f4 a4 f4 a4 a4 a4 a4 a5 a5 a5 i4 a10 a3 a5"
    rawdata = dl.loadDataFromCSV('Hilti_dataset_validation.csv',';',dataformat)
    
    cusprodq = rawdata[['CustomerID','ProductCode','NetSales']]
    cusprodq = pp.removeEntryByConstraint(cusprodq,lambda x:x['NetSales']<=0 or math.isnan(x['NetSales']))
    
    cuspurmat, d1mapping, d2mapping = pp.convert3DlistToMatrix(cusprodq,'CustomerID','ProductCode','NetSales')
    
    nnmodel = NearestNeighbors().fit(cuspurmat)
    pass

if __name__ == '__main__':
    main()