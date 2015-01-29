# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 19:14:29 2014



@author: qingwei
"""

from sklearn.neighbors import NearestNeighbors
from collections import Counter
from operator import itemgetter
from functools import reduce
import numpy as np


class Recommender:
    """
    A generic recommender class depends on UserProdPreference object
    Expose one function which is recommend(name,number)
    """    
    
    def __init__(self,userprodpreference):
        '''
        can only be initialized with userprodpreference object
        '''
        self.nnmodel = NearestNeighbors().fit(userprodpreference.spdata)
        self.datamodel = userprodpreference
        
    def recommend(self,name,number=5):
        '''
        public function to provide list of recommended products using knn
        note that this does not handle new user yet
        '''
        k_neighbor,distances = self.__kneighbors__(name)
        prods = self.__sortProducts__(k_neighbor,distances)
        
        return [prod[0] for prod in prods[:number]]
        # find a list of product to be recommended sorted in priority
        # use ranking to multiply the netsales
        
    def __sortProducts__(self,nearests_n,distance):
        '''
        private function to return a collection of products bought by knn
        the products is sorted by a combination of neighbor's distance with user
        and the products score relative to associated neighbor
        '''
        
        #distance should be processed, for instance we use %10 operation
        distance = [d%10 for d in distance]        
        
        # get list of user data in {prod1:score, prod2:score ...}
        usersdata = [self.datamodel.getUserDictByName(n) for n in nearests_n]
        
        # weight the score by dividing against corresponding distances
        weighteddata = [
            Counter({k:v/dist for k,v in user.items()}) for dist,user in zip(distance,usersdata)]
        
        # merge the list of dicts, handle key conflict by score summation        
        mergeddict = reduce(lambda x,y: x+y, weighteddata)
        
        # return sorted dict based on the
        return sorted(mergeddict.items(),key=itemgetter(1),reverse=True)
    
    def __kneighbors__(self,name,k=5):
        '''
        this function will return the nearest neighbors name
        '''
        
        uinfo = self.datamodel.getUserMatrixByName(name)
        u_dist,uids = self.nnmodel.kneighbors(uinfo,n_neighbors=k)
        
        # customer name is stored separated from the matrix, this code will retrieve it
        unames = [self.datamodel.users[uid] for uid in np.nditer(uids)]
        return unames[1:],u_dist.flatten().tolist()[1:]