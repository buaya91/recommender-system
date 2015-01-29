# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 13:44:37 2014

@author: qingwei
"""

import preprocessor as pp
import dataloader as dl

import numpy as np
from scipy.sparse import csr_matrix

class UserProdPreference():
    """
    this class will store users preferences of different products
    """
    
    def __init__(self, spdata,users,prods):
        '''
        default initialization accept sparse matrix where
        each row of matrix represent a user
        each col of matrix represent a prod
        value within represent degree of preferences
        '''
        self.spdata = spdata
        try:
            self.prods = [prod.decode() for prod in prods]
            self.users = [user.decode() for user in users]
        except(AttributeError):
            self.prods = prods
            self.users = users
        
    
    @classmethod
    def initFromCSVFile(cls,path,delimiter):
        '''
        initializae from File path
        file should be csv with 3 column, [user,prod,preference]
        '''
        df = 'a10 a10 f4'
        rawdata = dl.loadDataFromCSV(path,delimiter,df)
        return cls.initFromNumpyArray(rawdata)
        
    @classmethod
    def initFromSparseDataFile(cls,path):
        '''
        initialize from sparse data file stored in .npz
        the file should be saved using object method saveIntoNpz
        '''
        loader = np.load(path)
        spdata = csr_matrix((  loader['data'], loader['indices'], 
                             loader['indptr']), shape = loader['shape'])
        users = loader['users'].tolist()
        prods = loader['prods'].tolist()
        return cls(spdata,users,prods)
    
    @classmethod
    def initFromNumpyArray(cls,data):
        '''
        data should be numpy structured array with 3 columns
        [user,prod,preference]
        '''
        header = data.dtype.names
        spdata,user,prods = pp.convert3DlistToMatrix(data,header[0],
                                                    header[1],header[2])
        return cls(spdata,user,prods)
        
    def saveIntoNpz(self,filename):
        '''    # loop thru testupp.spdata
    # for every row, pick a nonzero feature and change it to zero
    # store the feature code
        save the object data into file, which can be use to reconstructed 
        the object using initFromSpareDataFile
        '''
        np.savez(filename,data = self.spdata.data,indices = self.spdata.indices,
                 indptr = self.spdata.indptr, shape = self.spdata.shape, 
                 users = self.users, prods = self.prods)
                 
    def updateUserData(self,user,product,value):
        '''
        update the user data inline, avoiding reconstruct the matrix
        '''
        uid = self.users.index(user)
        pid = self.prods.index(product)
        self.spdata[uid,pid] = value
        
    def getUserMatrixByName(self,user):
        '''
        return a 1-d matrix showing user's preferences of produc
        '''
        try:
            uid = self.users.index(user)
            return self.spdata[uid,:].todense()
        except(ValueError):
            raise ValueError("User does not exist in current dataset")

    def getUserDictByName(self,user):
        '''
        return a dict where each kv pair is product_id:preferences of user
        '''
        data = self.getUserMatrixByName(user)
        userprods = data.nonzero()[1]
        out = {self.prods[prod_idx]:data[0,prod_idx] for prod_idx in np.nditer(userprods)}
        return out
        
    def toBytes(self,s):
        try:
            s = s.encode()
            return s
        except(AttributeError):
            return s
    
    def toStr(self,s):
        try:
            s = s.decode()
            return s
        except(AttributeError):
            return s