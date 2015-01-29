# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 12:08:04 2014
provide function to clean data
@author: qingwei
"""

import csv
import copy
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import dok_matrix

def fRemoveColumnByIndex(source_path,destination_path,delimiter,col):
    """
    remove column of a csv file and create a new one, column can be text or 
    number

    """
    if(source_path == destination_path):
        raise ValueError("source and destination should be different")
    with open(source_path,"r") as sourcedata:
        datareader = csv.reader(sourcedata,delimiter=delimiter)
        with open(destination_path,"w") as result:
            datawriter = csv.writer(result)
            for row in datareader:
                del row[col]
                datawriter.writerow(row)
                
def fRemoveColumnByName(source_path,destination_path,delimiter,col):
    """
    remove column of csv by specifying name
    """
    if(source_path == destination_path):
        raise ValueError("source and destination should be different")
    with open(source_path,"r") as sourcedata:
        datareader = csv.DictReader(sourcedata,delimiter=delimiter)
        with open(destination_path,'w') as result:
            fn = copy.deepcopy(datareader.fieldnames)
            fn.remove(col)

            datawriter = csv.DictWriter(result,fn)
            datawriter.writeheader()
            for row in datareader:
                del row[col]
                datawriter.writerow(row)

def fRemoveEntryByConstraints(s_path, d_path, delimiter, constraint_func):
    """
    constraint_func(i):Boolean return true if i does not violate constraint
    """
    if(s_path == d_path):
        raise ValueError("source and destination should be different")
        
    def selectiveWrite(row):
        if(constraint_func(row)):
            datawriter.writerow(row)
                    
    with open(s_path,"r") as sourcedata:
        datareader = csv.DictReader(sourcedata,delimiter=delimiter)
        with open(d_path,"w") as result:
            datawriter = csv.DictWriter(result,datareader.fieldnames)
            datawriter.writeheader()
            map(selectiveWrite,datareader)
                
            
def removeFieldByName(dobj,*fieldnames):
    """
    return a view with fieldname removed
    """
    names = list(dobj.dtype.names)
    for fieldname in fieldnames:
        names.remove(fieldname)
    newobj = dobj[names]
    return newobj
    
def selectSpecificFieldByName(dobj, fieldnames):
    newobj = dobj[fieldnames]
    return newobj

def removeEntryByConstraint(dobj,constraint_func):
    """
    return a view that fulfill the constraint
    """
    pylist = [row for row in dobj if(constraint_func(row) == False)]
    newobj = np.empty(len(pylist),dtype=dobj.dtype)
    newobj[:] = pylist
    return newobj
    

def combineCols(dataobj,col1,col2,col3):
    '''
    dataobj is a numpy array, col1 and 2 will be combined to 3
    the output will be a dataobject with n-1 features
    '''
    # 1. normalize col1 and 2 (range is set to 0 to 100)
    # 2. combine them using col1+col2/2 and store as col 3
    # 3. remove col1 and 2
    # 4. append col3 and return
    mms = MinMaxScaler(feature_range=(0,100),copy=False)
    normalized1 = mms.fit_transform(dataobj[col1])
    normalized2 = mms.fit_transform(dataobj[col2])
    #create list so that we can append
    partA = removeFieldByName(dataobj,col1,col2)
    partB = (normalized1+normalized2)/2

    newdtype = [t for t in dataobj.dtype.descr if t[0] not in (col1,col2)]
    newdtype.append((col3,'<f4'))
    newdtype = np.dtype(newdtype)
    
    newobj = np.empty(len(dataobj),dtype=newdtype)
    
    tmplist = [tuple(list(a)+[b]) for a,b in zip(partA,partB)]
    newobj[:] = tmplist    
    
    return newobj

def convert3DlistToMatrix(dataobj,col1,col2,col3):
    """
    dataobj should be an array with three columnTiling arrays
tile(A, reps)	Construct an array by repeating A the number of times given by reps.
repeat(a, repeats[, axis])	Repeat elements of an array.

    only two column should be non-numeric, others should be numeric
    col1 and col2 should be name of non-numeric column
    a sparse matrix will be return
    """
    df = pd.DataFrame(dataobj).groupby([col1,col2]).sum()
    
    col1mp = list(np.unique(dataobj[col1]))
    col2mp = list(np.unique(dataobj[col2]))
    
    dim1len = len(col1mp)
    dim2len = len(col2mp)
    # for every row, pick a nonzero feature and     # loop thru testupp.spdata
    # for every row, pick a nonzero feature and change it to zero
    # store the feature codechange it to zero
    # store the feature codet
    matrix = dok_matrix((dim1len,dim2len),dtype=np.int16)
    for data in df.iterrows():
        idx1 = col1mp.index(data[0][0])
        idx2 = col2mp.index(data[0][1])
        matrix[idx1,idx2] = np.float16(data[1][col3])
        
    matrix = matrix.tocsr()
    return matrix,col1mp,col2mp
    












    