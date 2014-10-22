#!/usr/local/anaconda/bin/python2.7
'''
Created on Nov 2, 2013

@author: nancy
'''
import os, sys
import linesClass
import functionsClass
import trxFunctionsClass as trxFunc
import transitionsClass
import generalMethods as gm
import DEBUG_func as DEBUG

from datetime import datetime


func = functionsClass.Functions()
#trxFunc = TrxFunctionsClass.TrxFunctions()
#logHandler = linesClass.Logs()
global l; l=linesClass.l; 


def get_input_files(runType):
    if runType == 'big_test': 
        main_dir = '/home/michal/SALSA_files'
        source_dir = '/'.join([main_dir,'testFiles'])
        #Files = ['/home/michal/SALSA_files/testFiles/part-00000_150_12_03_10_first_100000_lines']
        Files = ['/'.join([source_dir,'part-00001_2_12_03_10_first_200000_lines'])]
                
    elif runType == 'small_test':
        main_dir = '/home/michal/SALSA_files'
        source_dir = '/'.join([main_dir,'testFiles'])
        Files = ['/'.join([source_dir,'part3_dummy_expanded'])]
        #Files = [ '/home/michal/SALSA_files/testFiles/part3_dummy_expanded']
        #Files = ['/home/michal/SALSA_files/testFiles/part-00000_150_12_03_10_first_100_lines'] #19 domains, no malwares
        #Files = ['/home/michal/SALSA_files/testFiles/part-00000_150_12_03_10_first_1000_lines'] #129 domains, no malweres, 329 edges
        #Files = ['/home/michal/SALSA_files/testFiles/part-00000_150_12_03_10_first_10000_lines']    #1020 domains, no malwares, 2724 edges
        
    else:   # runType == 'real_run'
        #main_dir = '/data'
        main_dir = '/data2'
        '''Files = ['/'.join([main_dir,'2/stats_12_03_10/part-00001']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00002']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00003']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00004']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00005']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00006']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00007']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00008']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00009']),\
                 '/'.join([main_dir,'2/stats_12_03_10/part-00010'])] '''
        Files = ['/'.join([main_dir,'2/stats_12_03_10/part-00001'])]  # 19673 domains, 6 malwares, 47593 edges
        '''NANCY FILES:
        Files = ['/data2/2/stats_12_03_10/part-00000',\
                 '/data2/2/stats_12_03_10/part-00048',\
                 '/data2/2/stats_12_03_11/part-00001',\
                 '/data2/2/stats_12_03_11/part-00010',\
                 '/data2/2/stats_12_03_13/part-00001',\
                 '/data2/2/stats_12_03_14/part-00001',\
                 '/data2/2/stats_12_03_15/part-00000',\
                 '/data2/2/stats_12_03_16/part-00000',\
                 '/data2/150/stats_12_03_15/part-00000',\
                 '/data2/150/stats_12_03_15/part-00001',\
                 '/data2/150/stats_12_03_10/part-00049']'''
        #Files = [ '/data/150/stats_12_03_10/part-00000']
        #Files = [ '/data/2/stats_12_03_10/part-00001','/data/2/stats_12_03_11/part-00001','/data/2/stats_12_03_12/part-00001','/data/2/stats_12_03_13/part-00001']
    
    blacklist_dir = '/'.join([main_dir,'blackLists'])
    malwareDomainsFile = '/'.join([blacklist_dir,'malwareDomains'])
    copyrightDomainsFile = '/'.join([blacklist_dir,'copyrightDomains'])
    
    return malwareDomainsFile, copyrightDomainsFile, Files
    
def get_output_files(runType,evaluated_domain_list=None):
    postfix = ''
    if evaluated_domain_list:
        evaluated_domains_str = '_'.join(evaluated_domain_list)
        postfix = ''.join(['_without_',evaluated_domains_str])
    
    main_dir = '/home/michal/SALSA_files/tmp/'
    '''out_dir = {'ginna_big_test':'big_test/',\
               'ginna_small_test':'small_test/',\
               'ginna':'real_run/'}'''
    
    processed_file= ''.join([main_dir,runType,'/input_list',postfix,'.csv'])
    output_users_risk_dict_path = ''.join([main_dir,runType,'/users_risk_dict',postfix,'.csv'])
    output_transitions_dict_path = ''.join([main_dir,runType,'/transitions_dict',postfix,'.csv'])
    output_domain_risk_dict_path = ''.join([main_dir,runType,'/domains_risk_dict',postfix,'.csv'])

    return processed_file, output_users_risk_dict_path, output_transitions_dict_path, output_domain_risk_dict_path
    

def main(run_mode, evaluated_domain_list=None,wo_users=False,link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.):
    print 'PREPROC: run mode- '+run_mode+', STRAT -----> ' + str(datetime.now()); sys.stdout.flush(); startTime = datetime.now()
    
    # initialize file for the  process
    malwareDomainsFile, copyrightDomainsFile, Files = get_input_files(run_mode)
    processedInputFile, users_risk_dict_path, transitions_dict_path, domain_risk_dict_path = get_output_files(run_mode,evaluated_domain_list)
    
    tmpTime = datetime.now()
    trxFunc.createRiskHashes(malwareDomainsFile,copyrightDomainsFile,ignore_domain_list=evaluated_domain_list)
    print '---main: createRiskHashes took: '+ str(datetime.now()-tmpTime); sys.stdout.flush()
    
    if os.path.exists(processedInputFile):
        func.importLinesFromFile(processedInputFile)
    else:       # First time- create the input processed list file
        # Populates lines (global) with the data from the log Files
        tmpTime = datetime.now()
        trxFunc.clear_lines()  #clear lines (from optional prev run data)  
        l.readSourceLogFiles(Files)
        print '---main: readSourceLogFiles took: '+ str(datetime.now()-tmpTime); sys.stdout.flush(); tmpTime = datetime.now()
        
        # Creates empty dictionaries with the appropriate aggregative columns 
        func.createDataContainersForUserAggregationProcess()
        print '---main: createDataContainersForUserAggregationProcess took: '+ str(datetime.now()-tmpTime); sys.stdout.flush(); tmpTime = datetime.now()
        
        trxFunc.addExtractedData_domainsGraph()
        print '---main: addExtractedData_domainsGraph took: ' + str(datetime.now()-tmpTime); sys.stdout.flush(); tmpTime = datetime.now()
        
        func.handelSessionsAndUserDataAggregation_domainsGraph(users_risk_dict_path)
        print '---main: handelSessionsAndUserDataAggregation_domainsGraph took: ' + str(datetime.now()-tmpTime)
        
        l.cleanLines()      # remove lines where shouldProcess = 0
        func.exportLinesToFile(processedInputFile)
    
    tmpTime = datetime.now()     
    if wo_users: # without users mode (simple graph) 
        import transitionsClass_wo_users as trans
        transitionsDict = trans.TransitionsDictObj
        transitionsDict.clear() #clear transitionsDict from optional prev run data
        transitionsDict.buildTransitionDict(l.lines,link_ref=link_ref,link_weight=link_weight)
    else:    # users mode- the graph weight is influenced by the users properties
        transitionsDict = transitionsClass.TransitionsDictObj
        transitionsDict.clear() #clear transitionsDict from optional prev run data
        usersRiskDict = gm.readDict(users_risk_dict_path)
        transitionsDict.buildTransitionDict(l.lines, usersRiskDict,link_ref=link_ref,link_weight=link_weight,redirect_ref=redirect_ref,redirect_weight=redirect_weight)
    transitionsDict.writeTransDictToFile(transitions_dict_path)
    transitionsDict.writeDomainRiskDictToFile(domain_risk_dict_path)
    print '---main: transitions creation took: ' + str(datetime.now()-tmpTime); sys.stdout.flush()
    
    print 'PREPROC FINISHED, Total Run Time:    '+str(datetime.now()-startTime); sys.stdout.flush()  
    return

'''def call_main():
    #run_mode = 'ginna_small_test'
    #run_mode = 'ginna_big_test'
    run_mode = 'ginna'    # real run
    main(run_mode)
    return

call_main()'''