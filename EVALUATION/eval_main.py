'''
Created on Aug 27, 2014

@author: michal
'''
import preproc_main as preproc
import salsa_main as salsa
from datetime import datetime
import sys


def run_entire_flow(run_mode,algorithms_list=[],mal_domains_list=[],wo_users=False,link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.):  
    print 'EVALUATION: run mode- '+run_mode+', STRAT -----> ' + str(datetime.now()); sys.stdout.flush();startTime = datetime.now() 
    if mal_domains_list:
        for d in mal_domains_list:
            preproc.main(run_mode, evaluated_domain_list=[d],wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight)
            salsa.main(run_mode, algorithms_list,evaluated_domain_list=[d])
    else:
        preproc.main(run_mode, evaluated_domain_list=[],wo_users=wo_users,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight)
        salsa.main(run_mode, algorithms_list,evaluated_domain_list=[])
    # TBD- run regular preproc and salsa for baseline ranks ?
    print '\n\nEVALUATION END: num of algorithms- '+str(len(algorithms_list))+', num of iterations per algorithm- '+str(len(mal_domains_list))+', total num of iterations- '+str(len(mal_domains_list)*len(algorithms_list))+'\nTOTAL RUN TIME: ' + str(datetime.now()-startTime); sys.stdout.flush()
    return

def run_preproc(run_mode,mal_domains_list=[]):
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
    return

    
def run_scores_histogram(run_mode,algorithms_list=[]):
    salsa.compare_scores_histogram(run_mode,algorithms_list)
    return

def main():
    run_mode='real_run'
    #run_mode='small_test'
    #run_mode='big_test'
    if run_mode == 'real_run':
        mal_domains_list = ['install.latestdl.info',\
                       'narod.ru',\
                       'click.readme.ru',\
                       'clck.ru',\
                       'allnokia.ru',\
                       'fion.ru']
        algorithms_list = ['salsa', 'hits', 'pagerank', 'inverse_pagerank'] #inverse RP changes the graph itself, hence should be last

    else:
        mal_domains_list = []#'allnokia.ru']
        algorithms_list = ['salsa']
    #algorithms_list = ['hits', 'pagerank', 'inverse_pagerank'] 
    #run_NANCY_flow(run_mode)
    run_entire_flow(run_mode,algorithms_list,mal_domains_list,redirect_ref=True,redirect_weight=0.5,link_ref=True,link_weight=0.2)#,wo_users=True)
    #run_preproc(run_mode,mal_domains_list)
    #run_salsa(run_mode,algorithms_list,mal_domains_list)
    #run_scores_histogram(run_mode,algorithms_list)
    return

main()