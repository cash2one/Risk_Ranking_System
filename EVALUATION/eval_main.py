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
import numpy as np

'''################## config parameters ##################'''

global run_mode;            run_mode = 'real_run'  # 'small_test' #   
global multiproc_flag;      multiproc_flag = True
global num_of_proc;         num_of_proc = 3   
global k_folds;             k_folds = 6
global algorithms_list;     algorithms_list = ['salsa', 'hits', 'pagerank', 'inverse_pagerank'] #inverse RP changes the graph itself, hence should be last
#global algorithms_list;     algorithms_list = ['hits', 'pagerank', 'inverse_pagerank']

global redirect_ref;        redirect_ref=True
global redirect_weight;     redirect_weight=0.5

global link_ref;            link_ref=True
global link_weight;         link_weight=0.2

global wo_users;            wo_users=False
global nstart_flag;         nstart_flag = True

'''######################################################'''


def run_entire_flow(run_mode,algorithms_list=[],tests_list=[],wo_users=False,\
                    link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.,\
                    nstart_flag=False,multiproc_flag=True):  
    '''
    Performs the flows in parallel  
    Parameters:
    -----------
        run_mode - str (small_test/real_run)
        algorithms_list - list of strs (default-[])
        tests_list - list of lists of numpy arrays [ [[d1,d2],[0,1]] , [[d3,d4],[1,0]] ] (default-[])
        wo_users - bool (default-False)
        link_ref - bool (default-False)
        link_weight - float (default-0.)
        redirect_ref - bool (default-False)
        redirect_weight - float (default-0.)
        nstart_flag - bool (default-False)
    Return:
    -------
        folds_stats_list - list of stats objects
    '''
    global num_of_proc
    print 'EVALUATION: run mode- '+run_mode+', STRAT -----> ' + str(datetime.now()); sys.stdout.flush();startTime = datetime.now() 
    if multiproc_flag:  #multiprocessing mode
        if len(tests_list):
                pool = Pool(processes=min(num_of_proc,len(tests_list)))
                #args_list = [ eval(''.join(['(\'',run_mode,'\',',str(algorithms_list),',[\'',d,'\'],',str(wo_users),',',str(link_ref),',',str(link_weight),',',str(redirect_ref),',',str(redirect_weight),')'])) \
                #             for d in mal_domains_list ]
                '''args_list = [ (run_mode,algorithms_list,[d],wo_users,link_ref,link_weight,redirect_ref,redirect_weight)\
                             for d in mal_domains_list ]'''
                args_list = [ (run_mode,algorithms_list,test,wo_users,link_ref,link_weight,redirect_ref,redirect_weight,nstart_flag,str(ind+1))\
                             for ind,test in enumerate(tests_list) ]
    
                folds_stats_list = pool.map(run_entire_flow_iteration_wrap,args_list)
        else:   # tests_list is empty
            folds_stats_list = [ run_entire_flow_iteration(run_mode,algorithms_list,tests_list,wo_users,link_ref,link_weight,redirect_ref,redirect_weight,nstart_flag) ]
    
    else:   # NOT multiprocessing mode (for debugging or "BL run"- e.g. got users risk scores from Nancy)
        folds_stats_list = []
        '''for idx,test in enumerate(tests_list):
            folds_stats_list.append(run_entire_flow_iteration(run_mode,algorithms_list,test,wo_users,link_ref,link_weight,redirect_ref,redirect_weight,nstart_flag) )
            '''
                
    print '\n\nEVALUATION END: num of algorithms- '+str(len(algorithms_list))+', num of iterations per algorithm- '+str(len(tests_list))+', total num of iterations- '+str(len(tests_list)*len(algorithms_list))+'\nTOTAL RUN TIME: ' + str(datetime.now()-startTime); sys.stdout.flush()
    return folds_stats_list 

def run_entire_flow_iteration(run_mode,algorithms_list=[],test=[],wo_users=False,link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.,nstart_flag=False,fold=None):
    '''
    Performs the flow  
    Parameters:
    -----------
        run_mode - str (small_test/real_run)
        algorithms_list - list of strs (default-[])
        test - list of numpy arrays [[d1,d2],[0,1]] (default-[])
        wo_users - bool (default-False)
        link_ref - bool (default-False)
        link_weight - float (default-0.)
        redirect_ref - bool (default-False)
        redirect_weight - float (default-0.)
        nstart_flag - bool (default-False)
    Return:
    -------
        fold_stats - stats object
    '''
    if fold:    f_postfix = ['fold',fold]
    else:       f_postfix = []
    outFile = gm.get_general_file_path(run_mode,'stdout',f_postfix,'outputs')
    sys.stdout = open(outFile,'w')
    
    eval_domains = []
    if len(test):
        eval_domains = test[0][np.where(test[1]==1)]
    preproc.main(run_mode, evaluated_domain_list=eval_domains,wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight,fold=fold)
    fold_stats = salsa.main(run_mode, algorithms_list,test=test,fold=fold,nstart_flag=nstart_flag)
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
    import stats
    import os
    startTime = datetime.now() 

    domains_risk_dict_f = gm.get_general_file_path(run_mode, 'mal_d/domains_risk', dir='tmp')
    
    # If the domains-label file not exist, run a 'full run' for creating the file (for stratified Kfolds)
    if not os.path.exists(domains_risk_dict_f):
        # run entire flow with empty evaluated domains list- will create the file of labeled domains risk dict (1=mal,0=else)
        run_entire_flow(run_mode,algorithms_list,[],\
                        redirect_ref=redirect_ref,redirect_weight=redirect_weight,\
                        link_ref=link_ref,link_weight=link_weight,\
                        nstart_flag=nstart_flag,wo_users=wo_users)
        #folds_stats_list =  run_entire_flow(run_mode,algorithms_list,[],wo_users=True)
    src_mal_domains = gm.get_general_file_path(run_mode, 'mal_d/src_mal_domains', dir='tmp') 
    mal_list = np.array(gm.read_list_from_file(src_mal_domains))#[line.strip() for line in open(src_mal_domains,'r')])
    '''if run_mode == 'real_run':  '''
    #mal_domains_list = []
    tests_list = []
    if len(mal_list):    #if src_mal_domains file not empty
        #kf = cross_validation.KFold(len(mal_list), n_folds=k_folds, shuffle=True)
        uzip_d_risk = zip(*gm.read_object_from_file(domains_risk_dict_f).items())
        kf = cross_validation.StratifiedKFold(list(uzip_d_risk[1]), n_folds=min(k_folds,sum(uzip_d_risk[1])))
        for train_index, test_index in kf:
            # test_dict is the test fold dict
            test = [np.asarray(uzip_d_risk[0])[test_index],np.asarray(uzip_d_risk[1])[test_index]]
            tests_list.append(test)
            #print test_dict; print 'XXXXX',len(tests_list),'\n',tests_list,'\n\n\n'
            #mal_domains_list.append(list(mal_list[test_index]))
       
    folds_stats_list =  run_entire_flow(run_mode,algorithms_list,tests_list,\
                                        redirect_ref=redirect_ref,redirect_weight=redirect_weight,\
                                        link_ref=link_ref,link_weight=link_weight,\
                                        nstart_flag=nstart_flag,wo_users=wo_users,\
                                        multiproc_flag=multiproc_flag)#,)
    #folds_stats_list =  run_entire_flow(run_mode,algorithms_list,mal_domains_list,redirect_ref=False)#,link_weight=1,wo_users=False)
    #folds_stats_list =  run_entire_flow(run_mode,algorithms_list,tests_list,wo_users=True)
    '''else:
        mal_domains_list = mal_list
        print mal_domains_list
        folds_stats_list =  run_entire_flow_iteration(run_mode,algorithms_list,mal_domains_list,redirect_ref=True,redirect_weight=0.5,link_ref=True,link_weight=0.2)#,wo_users=True)'''
    #run_scores_histogram(run_mode,algorithms_list)
    
    out_fn = gm.get_general_file_path(run_mode, 'eval_union_stats', dir='outputs')
    if len(folds_stats_list):   # if folds_stats_list not empty- means there was K fold cross validation run (not just BL)
        stats.stats_union(folds_stats_list, out_fn, raw_flag=True)
    print 'EVALUATION MAIN: Total time: ',startTime-datetime.now(); sys.stdout.flush()

    return

if __name__ == '__main__':
    main()