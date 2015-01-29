# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 14:36:54 2014
data loader
@author: qingwei
"""

import csv
import numpy as np
from scipy.sparse import csr_matrix

def convertData(data,dataformat):
    for idx,tp in enumerate(dataformat):
        if(tp.startswith('a')):
            data[idx] = str(data[idx])
        elif(tp.startswith('i')):
            data[idx] = int(data[idx])
        elif(tp.startswith('f')):
            data[idx] = float(data[idx])
        else:
            raise ValueError("type specific not supported")

    return tuple(data)

def loadDataFromCSV(path,delimiter,dataformat):
    """load data from csv and return corresponding list without header"""
    with open(path,'r') as datafile:
        datareader = csv.reader(datafile,delimiter = delimiter)
        header = datareader.__next__()
        dataformat = dataformat.split(' ')
        pylist = [convertData(row,dataformat) for row in datareader]
        dataobj = np.empty(len(pylist),dtype={'names':header,'formats':dataformat})
        dataobj[:] = pylist
        return dataobj
        
def loadHeaderFromCSV(path,delimiter,dataformat):
    with open(path,'r') as datafile:
        datareader = csv.reader(datafile,delimiter = delimiter)
        header = datareader.__next__()
        return header
        
def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )
             
def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])
                         
def saveNumpyAsCSV(filename, arr):
    with open(filename,'w') as f:
        writer = csv.writer(f,delimiter=',')
        ltol = []
        for idx,row in enumerate(arr):
            ltol.append([])
            for ele in row:
                try:
                    ltol[idx].append(ele.decode())
                except(AttributeError):
                    ltol[idx].append(ele)
        writer.writerows(ltol)
            
