'''
Created on Aug 28, 2014

@author: michal
'''
'''import math

mal_domain_list = [line.strip() for line in open("/home/michal/SALSA_files/tmp/small_test/test_domains",'r')] 
#['a','b','c','d','h','a','b','c','d','h','a','b','c','d','h','a','b','c','d','h','a','b','c','d','h','a','b','c']
num_of_folds = 5
if len(mal_domain_list)%num_of_folds>0 :
    n = len(mal_domain_list)/num_of_folds 
    #n = int( math.ceil( float(len(mal_domain_list) ) /num_of_folds ))
else:
    n = len(mal_domain_list)/num_of_folds 
#n=int( math.ceil( float(len(mal_domain_list) ) /num_of_folds ))
idx = 0

sublists = [mal_domain_list[x:x+n] for x in xrange(0, len(mal_domain_list), n)]
print len(mal_domain_list),len(sublists),sublists'''


from sklearn import cross_validation
import numpy as np


mal_list = np.array([line.strip() for line in open("/home/michal/SALSA_files/tmp/small_test/test_domains",'r')])  
kf = cross_validation.KFold(len(mal_list), n_folds=5)


for train_index, test_index in kf:
    eval_list = []
    print("TRAIN:", train_index, "TEST:", test_index)
    eval_list = mal_list[test_index] 
    print eval_list, len(eval_list)
    

