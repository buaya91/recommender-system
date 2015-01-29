#-------------------------------------------------------------------------------
# Name:        knn
# Purpose:     create k nearest neighbour from several source
#
# Author:      ASUS-PC
#
# Created:     22/09/2014
# Copyright:   (c) ASUS-PC 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# input will be user_similarity_matrix from several sources and also k
# output will be a list of nearest neighbour

from operator import itemgetter
from collections import Counter

def knn(user_similarity_matrix,user,k=2):
    '''
    return k nearest neighbor in list of (username,similarity)
    '''
    user_similarity_matrix[user].pop(user)
    sorted_similarity_list = sorted(user_similarity_matrix[user].items(),key=itemgetter(1),reverse=False)
    return sorted_similarity_list[:k]
    pass

def multi_source_knn(user,*user_similarity_matrixes,k=2):
    """
    construct k nearest neighbor from multiple table of similarity, each using different feature
    return a list of knn, element should looks like (username, similarity)
    """
    k_nearest_tuple = []
    for usm in user_similarity_matrixes:
        k_nearest_tuple.extend(knn(usm,user,k=k))

    k_nearest_user = [user[0] for user in k_nearest_tuple]

    user_count_pair = dict(Counter(k_nearest_user))
    k_user = sorted(user_count_pair.items(),key=itemgetter(1))

    return k_user[:k]
    pass
