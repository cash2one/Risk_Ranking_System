'''
Created on Aug 27, 2014

@author: michal
'''
import preproc_main as preproc
import salsa_main as salsa
import generalMethods as gm
from datetime import datetime
import sys
from multiprocessing import Pool

global num_of_proc; num_of_proc = 3
global run_mode; run_mode = 'small_test' #'real_run'  #
global k_folds; k_folds = 6
global algorithms_list; algorithms_list = ['salsa', 'hits', 'pagerank', 'inverse_pagerank'] #inverse RP changes the graph itself, hence should be last
#global algorithms_list; algorithms_list = ['hits', 'pagerank', 'inverse_pagerank']

def run_entire_flow(run_mode,algorithms_list=[],mal_domains_list=[],wo_users=False,link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.,nstart_flag=False):  
    global num_of_proc
    print 'EVALUATION: run mode- '+run_mode+', STRAT -----> ' + str(datetime.now()); sys.stdout.flush();startTime = datetime.now() 
    if mal_domains_list:
            pool = Pool(processes=num_of_proc)
            #args_list = [ eval(''.join(['(\'',run_mode,'\',',str(algorithms_list),',[\'',d,'\'],',str(wo_users),',',str(link_ref),',',str(link_weight),',',str(redirect_ref),',',str(redirect_weight),')'])) \
            #             for d in mal_domains_list ]
            '''args_list = [ (run_mode,algorithms_list,[d],wo_users,link_ref,link_weight,redirect_ref,redirect_weight)\
                         for d in mal_domains_list ]'''
            args_list = [ (run_mode,algorithms_list,d,wo_users,link_ref,link_weight,redirect_ref,redirect_weight,nstart_flag,str(mal_domains_list.index(d)+1))\
                         for d in mal_domains_list ]

            folds_stats_list = pool.map(run_entire_flow_iteration_wrap,args_list)
            
        #for d in mal_domains_list:
            #run_entire_flow_iteration(run_mode, evaluated_domain_list=[d],wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight,procName=d)
            #preproc.main(run_mode, evaluated_domain_list=[d],wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight)
            #salsa.main(run_mode, algorithms_list,evaluated_domain_list=[d])
    else:
        folds_stats_list = [ run_entire_flow_iteration(run_mode,algorithms_list,mal_domains_list,wo_users,link_ref,link_weight,redirect_ref,redirect_weight,nstart_flag) ]
        #preproc.main(run_mode, evaluated_domain_list=[],wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight)
        #salsa.main(run_mode, algorithms_list,evaluated_domain_list=[])
    # TBD- run regular preproc and salsa for baseline ranks ?
    print '\n\nEVALUATION END: num of algorithms- '+str(len(algorithms_list))+', num of iterations per algorithm- '+str(len(mal_domains_list))+', total num of iterations- '+str(len(mal_domains_list)*len(algorithms_list))+'\nTOTAL RUN TIME: ' + str(datetime.now()-startTime); sys.stdout.flush()
    return folds_stats_list 

def run_entire_flow_iteration(run_mode,algorithms_list=[],mal_domains_list=[],wo_users=False,link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.,nstart_flag=False,fold=None):
    if fold:    f_postfix = ['fold',fold]
    else:       f_postfix = []
    outFile = gm.get_general_file_path(run_mode,'stdout',f_postfix,'outputs')#mal_domains_list,dir='outputs')
    sys.stdout = open(outFile,'w')
    
    preproc.main(run_mode, evaluated_domain_list=mal_domains_list,wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight,fold=fold)
    fold_stats = salsa.main(run_mode, algorithms_list,evaluated_domain_list=mal_domains_list,fold=fold,nstart_flag=nstart_flag)
    return fold_stats
 
def run_entire_flow_iteration_wrap(args):
    return run_entire_flow_iteration(*args)
       
'''def run_preproc(run_mode,mal_domains_list=[]):
    print '\nrun_preproc- run mode: '+run_mode+'\n\nSTRAT -----> ' + str(datetime.now()); sys.stdout.flush();startTime = datetime.now() 
    
    for d in mal_domains_list:
        preproc.main(run_mode, evaluated_domain_list=[d])
    print '\nrun_preproc END: num of iterations- '+str(len(mal_domains_list))+'\nTOTAL RUN TIME: ' + str(datetime.now()-startTime); sys.stdout.flush()
    return

def run_salsa(run_mode,algorithms_list=[],mal_domains_list=[]):  
    print 'EVALUATION: run mode- '+run_mode+', STRAT -----> ' + str(datetime.now()); sys.stdout.flush();startTime = datetime.now() 
    if mal_domains_list:
        for d in mal_domains_list:
            salsa.main(run_mode, algorithms_list,evaluated_domain_list=[d])
    else:
        salsa.main(run_mode, algorithms_list)
    print '\n\nEVALUATION END: num of algorithms- '+str(len(algorithms_list))+', num of iterations per algorithm- '+str(len(mal_domains_list))+', total num of iterations- '+str(len(mal_domains_list)*len(algorithms_list))+'\nTOTAL RUN TIME: ' + str(datetime.now()-startTime); sys.stdout.flush()
    return

def run_NANCY_flow(run_mode):  
    print 'EVALUATION FOR NANCY: run mode- '+run_mode+', STRAT -----> ' + str(datetime.now()); sys.stdout.flush();startTime = datetime.now() 
    preproc.main(run_mode)
    salsa.main(run_mode, ['salsa'])
    print '\n\nEVALUATION FOR NANCY END: TOTAL RUN TIME: ' + str(datetime.now()-startTime); sys.stdout.flush()
    return'''

    
def run_scores_histogram(run_mode,algorithms_list=[]):
    salsa.compare_scores_histogram(run_mode,algorithms_list)
    return

def main():
    from sklearn import cross_validation
    import numpy as np
    import stats
    import os
    
    global run_mode, k_folds, algorithms_list
    
    # If the domains-label file not exist, run a 'full run' for creating the file (for stratified Kfolds)
    if not os.path.exists(gm.get_general_file_path(run_mode, 'mal_d/domains_risk', dir='tmp')):
        run_entire_flow(run_mode,algorithms_list,[],redirect_ref=True,redirect_weight=0.5,link_ref=True,link_weight=0.2)#,nstart_flag=True)#,wo_users=True)
    src_mal_domains = gm.get_general_file_path(run_mode, 'mal_d/src_mal_domains', dir='tmp') 
    mal_list = np.array([line.strip() for line in open(src_mal_domains,'r')])
    '''if run_mode == 'real_run':  '''
    mal_domains_list = []
    if len(mal_list):    #if src_mal_domains file not empty
        kf = cross_validation.KFold(len(mal_list), n_folds=k_folds, shuffle=True)
    
        for train_index, test_index in kf:
            mal_domains_list.append(list(mal_list[test_index])) 
    folds_stats_list =  run_entire_flow(run_mode,algorithms_list,mal_domains_list,redirect_ref=True,redirect_weight=0.5,link_ref=True,link_weight=0.2,nstart_flag=True)#,wo_users=True)
    #folds_stats_list =  run_entire_flow(run_mode,algorithms_list,mal_domains_list,redirect_ref=False)#,link_weight=1,wo_users=False)
    '''else:
        mal_domains_list = mal_list
        print mal_domains_list
        folds_stats_list =  run_entire_flow_iteration(run_mode,algorithms_list,mal_domains_list,redirect_ref=True,redirect_weight=0.5,link_ref=True,link_weight=0.2)#,wo_users=True)'''
    #run_scores_histogram(run_mode,algorithms_list)
    
    out_fn = gm.get_general_file_path(run_mode, 'eval_stats', dir='outputs')
    stats.stats_union(folds_stats_list, out_fn, raw_flag=True)
    return

if __name__ == '__main__':
    main()