#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 17, 2014

@author: michal

from /home/michal/SALSA_files/outputs run:
/usr/local/anaconda/bin/python2.7 /home/michal/workspace/SALSA_v1/mainModule.py > salsa_log &
'''

#import salsa 
#import networkx as nx
#import numpy as np
import generalMethods as gm
from datetime import datetime
import graph
#import DEBUG_func as DEBUG
import sys


#import matplotlib.pyplot as plt                 # For the graph plot

def get_input_files(run_mode,fold=None):
    import preproc_main as preproc
    transitions, domain_risk = preproc.get_output_files(run_mode, fold)[-2:]   # get last 2 elements returned from get_output_files
    return transitions, domain_risk
 
def get_output_files(run_mode,alg,evaluated_domain_list=None):       
    
    if 'pagerank' not in alg:   #hits or salsa
        output_hubs_file = gm.get_general_file_path(run_mode, '_'.join([alg,'hub']), post_list=evaluated_domain_list, dir='outputs')
        output_authorities_file = gm.get_general_file_path(run_mode, '_'.join([alg,'auth']), post_list=evaluated_domain_list, dir='outputs')
    else:   #pagerank or inverse_pagerank
        output_hubs_file = None
        output_authorities_file = gm.get_general_file_path(run_mode, alg, post_list=evaluated_domain_list, dir='outputs')

    return output_hubs_file, output_authorities_file


def main(run_mode='real_run',algorithms_list=[],test=[],fold=None,nstart_flag=False):                
    '''
    Performs the models flow 
    * IMPORTANT: algorithms_list- inverse RP changes the graph itself, hence should be last 
    Parameters:
    -----------
        run_mode - str (small_test/real_run) (default-'real_run')
        algorithms_list - list of strs (default-[])
        test - list of numpy arrays [[d1,d2],[0,1]] (default-[])
        fold - str ('1'/'2'/...) (default-None)
        nstart_flag - bool (default-False)
    Return:
    -------
        eval_obj - stats object
    '''
    import numpy as np
    
    test_mal = []
    if len(test):
        test_mal = test[0][np.where(test[1]==1)]
    print '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nALGORITHMS MAIN: \n\
    FOLD- ',fold,'\nevaluated domains- ',test_mal,'\nalg list- ',algorithms_list,'\nrun mode- ',run_mode,\
    '\nnstart_flag- ',nstart_flag,'\nSTRAT -----> ' ,datetime.now(); sys.stdout.flush(); startTime = datetime.now()                        
    
    if fold:    f_postfix = ['fold',fold]
    else:       f_postfix = None

    transitions_dict_path, domain_risk_dict_path = get_input_files(run_mode,fold)#evaluated_domain_list)
    whiteList_path = gm.get_general_file_path(run_mode, 'whiteList')

    G = graph.domains_graph(transitions_dict_path,domain_risk_dict_path,whiteList_path)
    
    #G.add_nodes_attr(G.n_attr.risk, gm.readDict(domain_risk_dict_path))
    #print '\nbefore preprocessing:'
    print '--- main: num of nodes: ' + str(G.G.number_of_nodes()) + ', num of edges: ' + str(G.G.number_of_edges()); sys.stdout.flush(); tmpTime=datetime.now()
    
    ''''G.graph_Preprocessing(gm.epsilon)
    print '\nafter graph preprocessing:'; sys.stdout.flush()
    DEBUG.print_num_of_nodes_with_in_deg_0(G.G)
    DEBUG.print_num_of_nodes_with_out_deg_0(G.G)
    print 'num of nodes: ' + str(G.G.number_of_nodes()) + '\nnum of edges: ' + str(G.G.number_of_edges()); sys.stdout.flush()
    '''
    risk_dict = None
    if nstart_flag:
        risk_dict = G.get_nodes_attr_val_dict(G.n_attr.risk)
    run = {'salsa':'G.run_salsa(salsa_type=\'salsa_per_class\')', \
               'hits':'G.run_hits(hits_type=\'hits\',nstart=risk_dict)', \
               'pagerank':'G.run_pagerank(pagerank_type=\'pagerank\',personalization=risk_dict)',\
               'inverse_pagerank':'G.run_pagerank(pagerank_type=\'pagerank\',personalization=risk_dict,inverse=True)'}
    
    for alg in algorithms_list:
        h,a = eval(run[alg])
        G.post_filtering_results(alg)
        hubs_file, authorities_file = get_output_files(run_mode,alg,f_postfix)#evaluated_domain_list)
        G.evaluate_algorithem(auth_fn=authorities_file, hub_fn=hubs_file, alg_type=alg)
        
        '''# write a and h dicts to files using pickle:
        a_fn = gm.get_general_file_path(run_mode,'_'.join([alg,'a_dict_pickle']),f_postfix)#evaluated_domain_list)
        gm.write_object_to_file(a, a_fn)'''
        #G.alg_histogram(alg)
        print '\n--- main: ',alg,' run + evaluation took: ',str(datetime.now()-tmpTime); sys.stdout.flush(); tmpTime = datetime.now()
    '''for n in evaluated_domain_list:
        #out_fn = get_general_file_path(run_mode,file_name='eval_out',evaluated_domain_list=[n],dir='outputs')
        out_fn = gm.get_general_file_path(run_mode,file_name='eval_out_sum',dir='outputs')
        G.write_eval_results_to_csv(evaluated_node=n,fn=out_fn)'''
    
    #print G.auc_evaluation(algorithms_list, test)#, fn)   
    # combined pure risk rank score dict:
    #generate_combined_scores(run_mode,algorithms_list,evaluated_domain_list)
    # combined lower percentage score dict:
    #G.create_combined_scores(run_mode, algorithms_list, evaluated_domain_list)   
   
    # In case of 'full run' we shall create output file of the mal domains and all domains with its rank as 0/1:
    if not fold:
        print '\n--- main: this is a FULL run!'
        out_fn = gm.get_general_file_path(run_mode,file_name='eval_BL_out',dir='outputs')
        eval_obj = G.evaluation(algorithms_list, test, out_fn) 
        # FOR DEBUG: gm.write_object_to_file(eval_obj, fn='/home/michal/SALSA_files/tmp/s_obj')
        G.export_domains_for_strat_Kfolds('/'.join(['/home/michal/SALSA_files/tmp',run_mode,'mal_d']))
    else:   # 'fold' run
        print '\n--- main: this is a FOLD run!'
        eval_obj = G.evaluation(algorithms_list, test)
        # export the iteration results to a weka file:
        fn_train = gm.get_general_file_path(run_mode, file_name='train', post_list=f_postfix, dir='outputs',file_type='.arff')
        fn_test = gm.get_general_file_path(run_mode, file_name='test', post_list=f_postfix, dir='outputs',file_type='.arff')
        fn_matrix = gm.get_general_file_path(run_mode, file_name='matrix', post_list=f_postfix, dir='outputs',file_type='.arff')
        G.export_to_weka_file(algorithms_list, test,fn_train,fn_test,fn_matrix)
    
    G.clear(); tmpTime = datetime.now()    #clean the graph and all it's attributes for (optional) next run
    
    
    
    print '\n--- main: evaluation took: ' , datetime.now()-tmpTime; sys.stdout.flush();
    print '\nALGORITHMS END.\tTotal run time: ' , datetime.now()-startTime; sys.stdout.flush()
    return eval_obj



def generate_combined_scores(run_mode,algorithms_list=[],evaluated_domain_list=None):
    startTime = datetime.now()
    dicts_list = []
    for alg in algorithms_list:
        dicts_list.append(gm.read_object_from_file( gm.get_general_file_path(run_mode,'_'.join([alg,'a_dict_pickle']),evaluated_domain_list) )) 

    combine_types = {'max': 'gm.create_max_dict_from_dicts(dicts_list)',\
                       'avg': 'gm.create_avg_dict_from_dicts(dicts_list)',\
                       'top_3_avg': 'gm.create_avg_dict_from_dicts(dicts_list,n=3)',\
                       'top_2_avg': 'gm.create_avg_dict_from_dicts(dicts_list,n=2)'}
    for k,v in combine_types.items():
        out_file = gm.get_general_file_path(run_mode,k,evaluated_domain_list,dir='outputs') 
        comb_score_dict = eval(v)
        u_pct_dict, l_pct_dict = gm.get_percentiles(comb_score_dict)
        gm.write_union_of_dicts_ordered_by_value_to_file(comb_score_dict, [u_pct_dict,l_pct_dict], out_file)
    print '\n--- main: combined scores generation and evaluation took: ' + str(datetime.now()-startTime); sys.stdout.flush();
    return

'''def call_main():
    #run_mode = 'small_test'
    #run_mode = 'big_test'
    run_mode = 'real_run'
    
    #alg = 'salsa'
    #alg = 'hits'
    #alg = 'pagerank'
    alg = 'inverse_pagerank'
    
    
    main(run_mode=run_mode, algorithm=alg)
    return

call_main()'''



def compare_scores_histogram(run_mode,algorithms_list=[],evaluated_domain_list=None):
    removed_domains_f = '/home/michal/SALSA_files/tmp/remove_domains_from_results'
    for alg in algorithms_list:
        
        print '\n--- main: '+alg; sys.stdout.flush()
        if 'pagerank' in alg:
            scores_dict = gm.read_object_from_file( gm.get_general_file_path(run_mode,'_'.join([alg,'a_dict_pickle']),evaluated_domain_list) )
            gm.histogram_of_dict(scores_dict, fn=removed_domains_f,bins=150)
        else:
            a_scores_dict = gm.read_object_from_file( gm.get_general_file_path(run_mode,'_'.join([alg,'a_dict_pickle']),evaluated_domain_list) )
            print '--- main: authorities'; sys.stdout.flush()
            gm.histogram_of_dict(a_scores_dict, fn=removed_domains_f,bins=150)
            print '\n--- main: combined'; sys.stdout.flush()
    scores_dict = combine_scores(algorithms_list)
    gm.histogram_of_dict(scores_dict, fn=removed_domains_f,bins=150)
            
        
    return

def combine_scores(algorithms_list,fn=None):
    dicts_list = []
    for alg in algorithms_list:
        dicts_list.append(gm.read_object_from_file( ''.join(['/home/michal/SALSA_files/tmp/real_run/',alg,'_a_dict_pickle']) )) 
    #dict_f = '/home/michal/SALSA_files/tmp/real_run/combined.csv'
    d = gm.create_max_dict_from_dicts(dicts_list)#, dict_f)
    
    u_pct_dict, l_pct_dict = gm.get_percentiles(d)
    #pct_dict_f = '/home/michal/SALSA_files/outputs/real_run/combined.csv'
    if fn:
        gm.write_union_of_dicts_ordered_by_value_to_file(d, [u_pct_dict,l_pct_dict], fn)#pct_dict_f)
    return d
