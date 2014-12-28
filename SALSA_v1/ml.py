'''
Created on Dec 15, 2014

@author: michal
'''
import numpy as np

class LR():
    def __init__(self,algs_list,scores_dicts_list,labels_dict,test):
        '''
        Parameters
        -----------
        algs_list - list of strs ['hits_auth','hits_hub'...]
        scores_dicts_list - list of dicts [{d1:23.5,d2:89.6...},{d1:2.5,d2:56.6...}...] 
            NOTE: the dicts ordered in the list according to algs_list order!
        labels_dict - dict (domain:label-0/1) {d1:0,d2:1,d3:0...} 
        test - list of numpy arrays [ nparray([d1,d2,d3...]) , nparray([0,1,0...]) ]
            test[0] = test domains 
            test[1] = test labels 
            
        Returns
        ---------
        None
        '''
        self.algs_list = algs_list
        n = len(labels_dict)
        names = ['domain'] + algs_list + ['label']
        domains = zip(*labels_dict.items())[0]
        max_len = len(max(domains,key=len))
        formats = ['a'+str(max_len)] + ['f4']*len(algs_list) + ['i4']
        self.m = np.zeros(n, dtype={'names':names, 'formats':formats})
        
        # update the actual label of the test domains in labels_dict:
        for idx,d in enumerate(test[0]):
            if test[1][idx]:    # if it's actual label isn't zero:
                labels_dict[d] = test[1][idx]
        
        # set the columns of m:
        self.m['domain'] = np.asarray(domains)
        for idx,alg in enumerate(algs_list):
            self.m[alg] = [scores_dicts_list[idx][d] for d in domains]
        self.m['label'] = [labels_dict[d] for d in domains]
        test_ind = np.in1d(self.m['domain'],test[0])
        self.test = self.m[test_ind]#[['domain']+algs_list]
        self.train = self.m[np.invert(test_ind)]#[algs_list]
        
        #DEBUG: print 'train\n',self.train,'\n\ntest:\n',self.test
        
        #dir = '/home/michal/SALSA_files/outputs/'
        #self.export_to_weka_file(fn_train=dir+'train.arff',fn_test=dir+'test.arff')
        return
    
    def export_to_weka_file(self,fn_train,fn_test):
        import csv
        header_a = '@relation sites_risk_rank\n'#@attribute \'domain\' real\n'
        header_b = []
        for alg in self.algs_list:
            header_b.append('@attribute \''+alg+'\' real\n')
        header_c = '@attribute \'label\' { 0, 1}\n@data'
        header = [header_a + ''.join(header_b) + header_c]

        f=open(fn_train, "wb")
        w = csv.writer(f, escapechar=' ',quoting=csv.QUOTE_NONE)
        w.writerow(header)
        for i in self.train[self.algs_list + ['label']]:
            w.writerow(i)
        f.close()
        
        f=open(fn_test, "wb")
        w = csv.writer(f, escapechar=' ', quoting=csv.QUOTE_NONE)
        w.writerow(header)
        for i in self.test[self.algs_list + ['label']]:
            w.writerow(i)
        f.close()
        return
    
    def export_matrix(self,fn):
        import generalMethods as gm
        gm.write_object_to_file(self.m, fn)
        return



'''#test:
algs_list = ['alg1','alg2']
d1 = {'abcdef':1.3,'b':2,'c':89.8,'d':97}
d2 = {'abcdef':5,'b':5.7,'c':0.2,'d':94.6}
d_list = [d1,d2]
labels = {'abcdef':0,'b':0,'c':0,'d':1}
test = [['b','c'],[1,0]]
lr = LR(algs_list,d_list,labels,test)
'''
