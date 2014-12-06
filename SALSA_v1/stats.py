'''
Created on Nov 11, 2014

@author: michal
'''
import numpy as np
class stats():
    
    #stats = {}
    
    def __init__(self,algs_list,Lpct_dicts_list):
        # the order of Lpct_dicts should be as the algs_list order!!
        self.stats = {} 
        for alg in algs_list:
            alg_Lpct_dict = Lpct_dicts_list[algs_list.index(alg)]
            self.stats[alg] = {'Lpct_dict' : alg_Lpct_dict,\
                               'Lpct_val_list' : np.array(zip(*sorted(alg_Lpct_dict.items()))[1])}    #list of the alg Lpct values ordered by domain
        self.domains_list = zip(*sorted(alg_Lpct_dict.items()))[0] # last alg_Lpct_dict (of the last alg)- all algs should have the exact same domains
        return
    
    def calc_stats(self):
        import generalMethods as gm
        for k,v in self.stats.items():
            Lpct_val_list = np.array(v['Lpct_val_list'])
            self.stats[k]['len'] = len(Lpct_val_list)
            self.stats[k]['min'] = min(Lpct_val_list)
            self.stats[k]['max'] = max(Lpct_val_list)
            self.stats[k]['avg'] = np.average(Lpct_val_list)
            self.stats[k]['median'] = np.median(Lpct_val_list)
            #self.stats[k]['var'] = np.var(Lpct_val_list)
            self.stats[k]['std'] = np.std(Lpct_val_list)
            self.stats[k]['#>80'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,80)
            self.stats[k]['%>80'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,80,pct_flag=True)
            self.stats[k]['#>85'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,85)
            self.stats[k]['%>85'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,85,pct_flag=True)
            self.stats[k]['#>90'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,90)
            self.stats[k]['%>90'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,90,pct_flag=True)
            self.stats[k]['#>95'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,95)
            self.stats[k]['%>95'] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,95,pct_flag=True)
        return
    
    def export_info(self,fn,raw_flag=False):
        # fn = (string) full path name of output file
        # raw_flag = (bool) is True for writing the raw data as well (Lpct values) 
        import csv
        ordered_attr = ['min','max','avg','median','std',\
                        '#>80','#>85','#>90','#>95',\
                        '%>80','%>85','%>90','%>95','len'] 
        f=open(fn, "wb")
        w = csv.writer(f)
        np.set_printoptions(precision=3)    # For printing numpy objects- prints 3 decimal after the point.
        w.writerow(['Algorithm'] + ordered_attr)
        for k,v in self.stats.items():
            w.writerow([k] + ["%.3f"%v[attr] for attr in ordered_attr])
        if raw_flag:    # writing the domains-Lpct dict
            w.writerow([' ']); w.writerow(['Lpct values'])
            w.writerow(['Domain']+sorted(self.stats))
            for d in self.domains_list:
                w.writerow([d]+["%.3f"%v['Lpct_dict'][d] for alg,v in sorted(self.stats.items())])
            '''for k,v in self.stats.items():
                w.writerow([' ']); w.writerow([k])
                w.writerow(['Domain','Lpct value'])
                for d,l in sorted(v['Lpct_dict'].items()):
                    w.writerow([d,"%.2f"%l])'''
        f.close()
        return
    
       
def stats_union(stats_list,fn,raw_flag=False):
    # stats_list = a list of stats objects
    if len(stats_list) == 1:    #In cases of NO K fold cross validation (evaluated domains list is empty)
        u_s = stats_list[0]
    else:   #K fold cross validation
        u_obj = stats_list[0].stats
        algs_list = u_obj.keys()
        u_dicts_list = [ u_obj[alg]['Lpct_dict'] for alg in algs_list ]
        for alg in algs_list:   # concatenate all Lpct dicts to the one of first object for each alg (saved as list of those dicts- u_dicts_list)
            idx = algs_list.index(alg)
            for s in stats_list[1:]:    # stats_list[0] already in u_dicts_list
                u_dicts_list[idx].update(s.stats[alg]['Lpct_dict'])  
        u_s = stats(algs_list,u_dicts_list)
        u_s.calc_stats()
    u_s.export_info(fn,raw_flag)
    return
    
            