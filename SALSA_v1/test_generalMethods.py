#!/usr/local/anaconda/bin/python2.7
'''
Created on Aug 10, 2014

@author: michal
'''
import generalMethods as gm

def test_check_if_stochastic_matrix():
    print '\t~~~ test_check_if_stochastic_matrix ~~~'
    '''stochastic_M = [[0.5,0.5,0],[0,0.7,0.3],[0.4,0,0.6]]
    if not gm.check_if_stochastic_matrix(stochastic_M):
        print 'error: check_if_stochastic_matrix returned False for a stochastic matrix'
    not_stochastic_M = [[0.5,0.5,0],[0.3,0.7,0.3],[0.4,0,0.6]]
    if gm.check_if_stochastic_matrix(not_stochastic_M):
        print 'error: check_if_stochastic_matrix returned True for a non-stochastic  matrix'
    '''
    # STOCHASTIC cases:
    # we won't have cases where the whole matrix contains ints only (eps values from Self Links or Central Node connection)!!!
    # case- stochastic matrix that only one of it's elements is float (all other ints):
    stochastic_M_np = np.matrix([[1,0,0],[0,1.,0],[0,0,1]])
    if not gm.check_if_stochastic_matrix(stochastic_M_np):
        print 'error: check_if_stochastic_matrix returned False for a stochastic numpy matrix (case: init with int and float)'
    # case- stochastic float matrix:
    stochastic_M_np = np.matrix([[0.5,0.5,0],[0,0.7,0.3],[0.4,0,0.6]])
    if not gm.check_if_stochastic_matrix(stochastic_M_np):
        print 'error: check_if_stochastic_matrix returned False for a stochastic numpy matrix (case: init with float)'
    
    # NOT STOCHASTIC cases:
    # case- row sum greater than 1:
    not_stochastic_M_np = np.matrix([[0.5,0.5,0],[0.3,0.7,0.3],[0.4,0,0.6]])
    if gm.check_if_stochastic_matrix(not_stochastic_M_np):
        print 'error: check_if_stochastic_matrix returned True for a non-stochastic numpy matrix (case: row sum greater than 1)'
    # case- row sum less than 1:
    not_stochastic_M_np = np.matrix([[0.5,0.5,0],[0,0.7,0.3],[0,0,0]])
    if gm.check_if_stochastic_matrix(not_stochastic_M_np):
        print 'error: check_if_stochastic_matrix returned True for a non-stochastic numpy matrix (case: row sum less than 1)'
        
    print '\t~~~ FINISHED test_check_if_stochastic_matrix ~~~'
    return

def test_convert_SL_and_CN_weights_to_val():
    import numpy as np
    import scipy.sparse as sps
    
    print '\t~~~ test_convert_SL_and_CN_weights_to_val ~~~'
    A = np.matrix([[1.,0,0,0],\
                   [0,1.,0,0],\
                   [0,0,1.,0],\
                   [0,0,0,1.]])
    A = sps.csr_matrix(A)
    ''''v = np.asarray([1,1,1,1])
    A_col3 = A[:,3].todense()
    A3 = A.getcol(3)
    A3_set = A.setcol(3,v)
    A[:,3] =  A_col3 + v.T'''
    #A = sps.lil_matrix(A)
    A =  gm.convert_SL_and_CN_weights_to_val(A, val=0.2, CN_idx=2, stochastic_out=True)
    print A
    print A.todense()
    print '\t~~~ FINISHED test_convert_SL_and_CN_weights_to_val ~~~'
    return


def test_get_percentiles():
    d = {'a':1, 'b':2, 'c':3, 'd':3, 'e':4}
    print gm.get_percentiles(d)
    return

def test_write_union_of_dicts_ordered_by_value_to_file():
    d = {'a':1, 'b':2, 'c':3, 'd':3, 'e':4}
    u,l = gm.get_percentiles(d)
    fn = '/home/michal/SALSA_files/tmp/test_out'
    gm.write_union_of_dicts_ordered_by_value_to_file(d, [u,l,d], fn)
    return

def test_distribution_plot():
    import random
    gm.distribution_plot(random.sample(range(300),10),10)
    return

def test_create_avg_dict_from_dicts():
    d1 = {'a':7,'b':2,'c':12}
    d2 = {'a':5,'b':11,'c':1}
    d3 = {'a':10,'b':2,'c':3}
    dicts_list = [d1,d2,d3]
    print gm.create_avg_dict_from_dicts(dicts_list,n=2)
    return

def test_create_max_dict_from_dicts():
    d1 = {'a':7,'b':2,'c':12}
    d2 = {'a':5,'b':11,'c':1}
    d3 = {'a':10,'b':2,'c':3}
    dicts_list = [d1,d2,d3]
    print gm.create_max_dict_from_dicts(dicts_list)
    return
    
def test_salsa_main_get_general_output_file():
    import salsa_main as sls
    print sls.get_general_output_file('real_run', 'TEST', ['ignore1','ignore2'], 'tmp')
    return

def test_write_append():
    import csv, numpy as np
    fn = '/home/michal/SALSA_files/tmp/test2.csv'
    d = {'one':{'a':1,'b':6,'c':3,'d':5},'two':{'a':2,'b':7,'c':4,'d':6},'three':{'a':3,'b':8,'c':5,'d':7}}
    sub_d = {'a':1,'b':6,'c':3,'d':5}
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
        w.writerow(['---------------------------------'])
        w.writerow(['---------------------------------'])
        w.writerow(['---------------------------------'])
        attrs,vals = zip(*sorted(sub_d.items()))
        w.writerow([n]+list(attrs))
        w.writerow([n]+list(vals))
    return
    
def main():
    #test_check_if_stochastic_matrix()
    #test_convert_SL_and_CN_weights_to_val()
    #test_get_percentiles()
    #test_write_union_of_dicts_ordered_by_value_to_file()
    #test_scores_dist_plot()
    #test_create_max_dict_from_dicts()
    #test_create_avg_dict_from_dicts()
    #test_salsa_main_get_general_output_file()
    test_write_append()
    return

main()