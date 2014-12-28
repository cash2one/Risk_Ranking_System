#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 20, 2014

@author: michal
'''
import csv
from operator import itemgetter

def read_list_from_file(fn):
    return [ line.strip() for line in open(fn,'r') ]    # does not recognize 'close', so probably close by the end of the func anywat...
 
def write_list_to_file(l,fn):
    f=open(fn, "wb")
    w = csv.writer(f)
    for element in l:
        w.writerow([element])
    f.close()

def saveDict(fn,dict_rap):
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in dict_rap.items():
        w.writerow([key, val])
    f.close()
     
def readDict(fn):
    import sys
    maxInt = sys.maxsize
    decrement = True
            
    f=open(fn,'rb')
    dict_rap={}
    while decrement:
        decrement = False          
        try:
            csv.field_size_limit(maxInt)
            for key, val in csv.reader(f):
                dict_rap[key]=eval(val)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
        
    f.close()
    return(dict_rap)

def print_dict(d):
    for key in d.keys():
        print str(key) + ' : ' + str(d[key].round(4))
    return 

def print_dict_ordered_by_value(d):
    i=1
    for k, v in sorted(d.items(), key=itemgetter(1), reverse=True):
        #print str(i) + ':\t' + str(k) + '-\t' + str(v.round(4))
        print '(' + str(i) + ')\t' + str(k) + ':\t\t' + str(round(v,4))
        i+=1
    return

def write_dict_ordered_by_value_to_file(d,fn):
    i=1
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in sorted(d.items(), key=itemgetter(1), reverse=True):
        w.writerow([i, key, val])
        i+=1
    f.close()
    return

def write_union_of_dicts_ordered_by_value_to_file(d,dicts_list,fn):
    # d = dict where the output is order by its values!
    # dicts_list = list of all dicts where its value is added to the ordered d (as the input)
    # IMPORTANT: dicts_list MUST include AT LEAST 2 dicts!!!
    # fn = file name (with full path) for the output
    i=1
    f=open(fn, "wb")
    w = csv.writer(f)
    for key, val in sorted(d.items(), key=itemgetter(1), reverse=True):
        w.writerow([key, val] + [dict_i[key] for dict_i in dicts_list[:-1]] + ['#', dicts_list[-1][key]])
        i+=1
    f.close()
    return
# general parameters:

def writeMatrixToFile(filePath, matrix):
    import os
    os.path.exists(filePath) and os.remove(filePath)
    target = open(filePath, 'a')
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            target.write(str(matrix[i][j])) ;
            target.write(str("\t")) ;
        target.write("\n")
    target.close();
                
    return 


def l1_norm_vector(V):
    # V is array
    return V/sum(V) 

def convert_all_matrix_zeros_to_val(M,val,stochastic_out=False):
    # M is a SPARSE matrix
    # val is the value you wish to fill instead all zeroes in M
    # is_sparse = is M sparse? (True/False)
    # stochastic_out = pass True if you wish the returned matrix be stochastic (each row sums to 1)
    # returns the new matrix M (with no zeros)
    from sklearn.preprocessing import normalize     # For normalizing matrix by row (sums to 1)

    '''if is_sparse:
        M = M.todense()
    P = np.asmatrix(M)'''
    M = M.todense()
    M += val
    '''for x in np.nditer(P,op_flags=['readwrite']):   #flags=['refs_ok'],
        x[...] = max(x,val)'''
    if stochastic_out:
        normalize(M, axis=1, norm='l1')   
    return M

def convert_upper_triangle_to_val(M,val):
    # M is a SPARSE matrix
    # val is the value you wish to fill instead all zeroes in M
    for i in range(M.shape[0]-1):
        for j in range(i+1,M.shape[0]-1-i):
            if not M[i,j]: M[i,j] = val
    return M

def convert_SL_and_CN_weights_to_val(M,val,CN_idx,stochastic_out=False):
    # M is a SPARSE matrix
    # val is the value you wish to fill instead all zeroes in M
    # is_sparse = is M sparse? (True/False)
    # stochastic_out = pass True if you wish the returned matrix be stochastic (each row sums to 1)
    # returns the new matrix M (with no zeros)
    import sys
    from datetime import datetime
    startTime = datetime.now()       
    import scipy.sparse as sps
                     

    print '\n\t~~~~~~ generalMethods: convert_SL_and_CN_weights_to_val (M, val='+str(val)+', CN_idx='+str(CN_idx)+', stochastic_out='+str(stochastic_out)+') ~~~~~~'; sys.stdout.flush()
    '''for i in xrange(M.shape[0]-1):
        #if not M[i,i]: M[i,i] = val
        if not M[CN_idx,i]: M[CN_idx,i] = val
        if not M[i, CN_idx]: M[i, CN_idx] = val
    '''
    from sklearn.preprocessing import normalize     # For normalizing matrix by row (sums to 1)

    M = sps.lil_matrix(M)   # just for updating the sparse matrix M (changing csr_matrix is expensive!)
    for i in xrange(M.shape[0]):  
        M[CN_idx, i] = max(val, M[CN_idx, i])
        M[i, CN_idx] = max(val, M[CN_idx, i])
    M = sps.csr_matrix(M)
    print '\n--- generalMethods: convert_SL_and_CN_weights_to_val: for loop took: ' + str(datetime.now()-startTime); sys.stdout.flush()
    #M = convert_upper_triangle_to_val(M,val)
    if stochastic_out:
        return normalize(M, axis=1, norm='l1', copy=False)   
    return M

def check_if_stochastic_matrix(np_mat):
    # np_mat is a numpy matrix, which its elements are FLOAT and  NOT INT!!!
    # returns: True/False
    is_stochastic = True
    for i in range(len(np_mat)):
        if str(np_mat[i].sum()) != '1.0':
            is_stochastic = False
            break
    return is_stochastic    
        

'''def write_graph_to_file(G,fn):
    import pickle
    pickle.dump(G, open(fn, 'w'))
    return

def read_graph_from_file(fn):
    import pickle
    return pickle.load(open(fn))'''

def write_object_to_file(obj,fn):
    import pickle
    pickle.dump(obj, open(fn, 'w'))
    return

def read_object_from_file(fn):
    import pickle
    return pickle.load(open(fn))


def get_percentiles(src_dict):
    from scipy.stats import stats as spst
    K,V = zip(*(list(sorted(src_dict.items(), key=itemgetter(1))))) # unzip the ordered src_dict
    u_pct = [spst.percentileofscore(V,v,kind='weak') for v in V]    # upper percentile list (under OR EQUAL)
    l_pct = [spst.percentileofscore(V,v,kind='strict') for v in V]  # lower percentile list (under)
    u_pct_dict = dict(zip(K,map(float,u_pct)))
    l_pct_dict = dict(zip(K,map(float,l_pct)))
    return u_pct_dict, l_pct_dict

def histogram_of_dict(d,fn,bins=200):
    from matplotlib import pyplot as plt
    d = clean_scores_dict(d,fn)
    print max(d.values())
    #plt.bar(range(0,10),d)#.values())
    #, range, normed, weights, cumulative, bottom, histtype, align, orientation, rwidth, log, color, label, stacked, hold)
    #print d;
    plt.hist(d.values(), bins=bins, normed=True, log=True)#stacked=True, cumulative=False)
    plt.show()
    
    return

def clean_scores_dict(d,fn):
    # Deletes elements from dict, where the deleted keys appear in a file
    # d = dict
    # fn = full path of the file containing the list of required removed keys
    with open(fn,'r') as f:
        remove_keys = f.readlines()
    remove_keys = [k.rstrip() for k in remove_keys]
    for k in remove_keys:
        del d[k]
    return d


def create_combined_score(comb_type,dicts_list,is_last_dict_risk=False,fn=None):
    # dicts_list = list of dictionaries 
    # is_last_dict_risk = True if the last element in dicts_list is the init risk rank dict
    # comb_type = (str) type of combination: max, avg, top2_avg, top3_avg
    # fn = full path of output file
    
    combine_types = {'max': 'create_max_dict_from_dicts(dicts_list)',\
                   'avg': 'create_avg_dict_from_dicts(dicts_list)',\
                   'top3_avg': 'create_avg_dict_from_dicts(dicts_list,n=3)',\
                   'top2_avg': 'create_avg_dict_from_dicts(dicts_list,n=2)'}
    comb_score_dict = eval(combine_types[comb_type])
    u_pct_dict, l_pct_dict = get_percentiles(comb_score_dict)
    if is_last_dict_risk:
        write_union_of_dicts_ordered_by_value_to_file(comb_score_dict, [u_pct_dict,l_pct_dict,dicts_list[-1]], fn)
    else:
        write_union_of_dicts_ordered_by_value_to_file(comb_score_dict, [u_pct_dict,l_pct_dict], fn)
    return
        
def create_max_dict_from_dicts(dicts_list,threshold=0,fn=None):
    # dicts_list = list of dictionaries WHICH HAVE THE SAME KEIS!!!!!
    # fn = output file path
    d = {}
    if threshold > 0:
        for key in dicts_list[0]:
            max_val = max([dict_i[key] for dict_i in dicts_list])
            if max_val > threshold: d[key] = max_val
            else: d[key] = min([dict_i[key] for dict_i in dicts_list])
    else:
        for key in dicts_list[0]:
            d[key] = max([dict_i[key] for dict_i in dicts_list])
    if fn:
        write_dict_ordered_by_value_to_file(d,fn)
    return d

def create_avg_dict_from_dicts(dicts_list,n=None,fn=None):
    # dicts_list = list of dictionaries WHICH HAVE THE SAME KEIS!!!!!
    # n = the average is made from the top n values
    # fn = output file path
    import numpy as np
    
    d = {}
    if not n:
        n = len(dicts_list)
    for key in dicts_list[0]:
        d[key] = np.mean(sorted([dict_i[key] for dict_i in dicts_list],reverse=True)[0:n])  # [0:n] is NOT including n!!!
    if fn:
        write_dict_ordered_by_value_to_file(d,fn)
    return d


def write_dict_of_dicts_to_file(d,fn,first_col_name='domain'):
    # d is a dict of dicts
    # fn is the full path of the output file
    import csv
    #fn = '/home/michal/SALSA_files/tmp/test2.csv'
    d = {'one':{'a':1,'b':6,'c':3,'d':5},'two':{'a':2,'b':7,'c':4,'d':6},'three':{'a':3,'b':8,'c':5,'d':7}}
    n = 'doamin'
    sorted_dom_list = sorted(d)
    
    with open(fn, "a") as f:
        w = csv.writer(f)
        w.writerow(['---------------------------------'])
        w.writerow([n]+[attr for attr in sorted(d[sorted_dom_list[0]])])
        for k in sorted_dom_list:
            #print zip(*sorted(d.items()))[1]
            #w.writerow([k]+[attr for attr in sorted(d[k])])
            w.writerow([k]+list(zip(*sorted(d[k].items()))[1]))
    return

def get_general_file_path(run_mode,file_name,post_list=None,dir='tmp',file_type='.csv'): 
    ''' 
    Parameters
    -----------
    run_mode - string, the directory name- 'small_test'/'real_run' 
    file_name - string, the file (prefix) name
    post_list - list of STRINGS (default None)
    dir - string, directory name (default 'tmp')
    file_type - string, file ending (default '.csv')
    
    Returns
    -------
    the joined full path (/home/michal/SALSA_files/ dir/ run_mode/ file_name_+post_list+file_type)
    '''      
    postfix = ''
    if post_list:
        #post_list_str = '_'.join(post_list)
        postfix = ''.join(['_','_'.join(post_list)])#''.join(['_without_',evaluated_domains_str])
    
    main_dir = '/home/michal/SALSA_files'
    return '/'.join([main_dir,dir,run_mode,''.join([file_name,postfix,file_type])])

def calc_elements_greater_than_threshold(l,threshold,pct_flag=False):
    ans = sum(i>=threshold for i in l)
    if pct_flag:    # the return val is in percentage units
        return float(ans)/len(l)
    else:   # the returned val is the actual number of elements
        return ans
    
def get_labels_dict_from_dict(d,threshold=1):
    ''' convert a dict of keys-vals to keys-labels (0,1)
    Parameters
    -----------
    d - dict with float/int values
    threshold - float/int, when the dict val >= threshold --> label=1, else lavel=0
    Returns
    -------
    labeled dict keys-labels
    '''
    #[keys,values] = zip(*d.items())
    D = d.copy()
    for k,v in D.items():
        if v >= threshold:
            D[k] = 1
        else:
            D[k] = 0
    return D

epsilon = 1e-4 #0.0001
risk_threshold = 0.1 #when a node (domain) initial risk rank is greater or equal to this value- it is labeled as risky node 