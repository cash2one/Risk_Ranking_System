'''
Created on Nov 11, 2014

@author: michal
'''
import numpy as np

class stats_alg_atributes():
    num_of_mal = 'num_of_mal'
    min = 'min'
    max = 'max'
    avg = 'avg'
    median = 'median'
    std = 'std'
    g80 = '#>80'
    pct_g80 = '%>80'
    g85 = '#>85'
    pct_g85 = '%>85'
    g90 = '#>90'
    pct_g90 = '%>90'
    g95 = '#>95'
    pct_g95 = '%>95'
    auc = 'auc'
    num_of_test_domains = 'num_of_test_domains'
    
    
class stats():
        
    def __init__(self,algs_list,Lpct_dicts_list,label_list=[],scores_list=[]):
        ''' initiate of stats object
        Parameters
        -----------
        algs_list - list of algorithm names (strings) 
        Lpct_dicts_list - list of the Lpct scores (dict of 'domain':<Lpct_score>)
            NOTE: the order of Lpct_dicts should be as the algs_list order!!
        label_list - list of labels (0/1) of the TEST set, [0,1,0,1,1,...] (default empty list [])
        scores_list - list of scores list of the TEST set, [ [45.5,8.3,..], [59.6,99.7,...], ... ] 
            (default empty list [])
            NOTE: the order of the scores lists should be as the algs_list order!!
                  the inner order of the elements in each scores list should match the (domains order of) label_list
        Returns
        --------
        None
        '''
        self.atr = stats_alg_atributes()
        self.test_labels = np.asarray(label_list)
        self.stats = {} 
        for idx,alg in enumerate(algs_list):
            alg_Lpct_dict = Lpct_dicts_list[idx]
            # Lpct_val_list - list of the alg Lpct values of the risky domains ONLY (label=1) ordered by domain
            # test_scores_list - list of the alg Lpct of ALL domains
            self.stats[alg] = {'Lpct_dict' : alg_Lpct_dict,\
                               'Lpct_val_list' : np.array(zip(*sorted(alg_Lpct_dict.items()))[1]),\
                               'test_scores_list': np.asarray(scores_list[idx])}    
        self.domains_list = zip(*sorted(alg_Lpct_dict.items()))[0] # last alg_Lpct_dict (of the last alg)- all algs should have the exact same domains
        return
    
    def calc_stats(self):
        import generalMethods as gm
        from sklearn.metrics import roc_auc_score
        #from sklearn.metrics import classification_report
        
        for k,v in self.stats.items():  # for each alg:
            Lpct_val_list = np.array(v['Lpct_val_list'])
            self.stats[k][self.atr.num_of_mal] = len(Lpct_val_list)
            self.stats[k][self.atr.min] = min(Lpct_val_list)
            self.stats[k][self.atr.max] = max(Lpct_val_list)
            self.stats[k][self.atr.avg] = np.average(Lpct_val_list)
            self.stats[k][self.atr.median] = np.median(Lpct_val_list)
            self.stats[k][self.atr.std] = np.std(Lpct_val_list)
            self.stats[k][self.atr.g80] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,80)
            self.stats[k][self.atr.pct_g80] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,80,pct_flag=True)
            self.stats[k][self.atr.g85] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,85)
            self.stats[k][self.atr.pct_g85] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,85,pct_flag=True)
            self.stats[k][self.atr.g90] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,90)
            self.stats[k][self.atr.pct_g90] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,90,pct_flag=True)
            self.stats[k][self.atr.g95] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,95)
            self.stats[k][self.atr.pct_g95] =  gm.calc_elements_greater_than_threshold(Lpct_val_list,95,pct_flag=True)
            self.stats[k][self.atr.auc] = roc_auc_score(self.test_labels, v['test_scores_list'])
            self.stats[k][self.atr.num_of_test_domains] = len(v['test_scores_list'])
            
            # for the following you shall choose a threshold!!:
            #print classification_report(self.test_labels, v['test_scores_list'], target_names=['class 0', 'class 1']) # precision, recall, f1-score, support

        return
    
    def export_seed_histogram(self,fn):
        '''export the histogram of seed (label 1 domains) of all algs to file)'''
        import matplotlib.pyplot as plt
        import matplotlib as mpl

        # These are the "Tableau 20" colors as RGB.  
        tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                     (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
                     (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
                     (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
                     (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
          
        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
        for i in range(len(tableau20)):  
            r, g, b = tableau20[i]  
            tableau20[i] = (r / 255., g / 255., b / 255.)  
        
        ranks = []  # list of the algs seed ranks lists, [ [3,55,46] , [35,88,67] , ... ]
        algs = []
        for alg,val in self.stats.items():
            algs.append(alg)
            ranks.append(val['Lpct_val_list'])
        '''seed_idxs = np.where(self.test_labels == 1)[0]
        for k,v in self.stats.items():  # for each alg:
            algs.append(k)
            ranks.append(v['test_scores_list'][seed_idxs])'''
        
        
        '''y0,binEdges=np.histogram(ranks[0],bins=10)
        y1,binEdges=np.histogram(ranks[1],bins=10)
        y2,binEdges=np.histogram(ranks[2],bins=10)
        y3,binEdges=np.histogram(ranks[3],bins=10)
        y4,binEdges=np.histogram(ranks[4],bins=10)
        y5,binEdges=np.histogram(ranks[5],bins=10)
        binEdges=np.histogram(ranks[0],bins=10)[1]'''
        # I did it ugly and manually cause there were problems with the for implementation (np.histogram)!
        # NOTE: if number of algs ranks is changing you need to update this code accordingly!
        y0,binEdges = np.histogram(ranks[0],bins=10, normed=True)
        y1 = np.histogram(ranks[1],bins=10, normed=True)[0]
        y2 = np.histogram(ranks[2],bins=10, normed=True)[0]
        y3 = np.histogram(ranks[3],bins=10, normed=True)[0]
        y4 = np.histogram(ranks[4],bins=10, normed=True)[0]
        y5 = np.histogram(ranks[5],bins=10, normed=True)[0]

        #bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        for idx,alg in enumerate(algs):
            if alg.startswith('inv'): algs[idx]='inv_pagerank'
            if alg.startswith('page'): algs[idx]='pagerank'
            
        
        alg0 = algs[0]
        alg1 = algs[1]
        alg2 = algs[2]
        alg3 = algs[3]
        alg4 = algs[4]
        alg5 = algs[5]
        
        plt.figure(facecolor="white")
        
        plt.plot(y0,'-', label=alg0,lw=1.5, color=tableau20[0])
        plt.plot(y1,'-', label=alg1,lw=1.5, color=tableau20[2])
        plt.plot(y2,'-', label=alg2,lw=1.5, color=tableau20[4])
        plt.plot(y3,'-', label=alg3,lw=1.5, color=tableau20[6])
        plt.plot(y4,'-', label=alg4,lw=1.7, color=tableau20[8])
        plt.plot(y5,'-', label=alg5,lw=1.7, color=tableau20[16])
        '''for i in ranks:
            plt.plot(bincenters,np.histogram(ranks[i],bins=10)[0],'-', label=algs[i])'''
        
        '''plt.plot(bincenters,y0,'-', bincenters,y1,'r-', bincenters,y2,'g-',\
                 bincenters,y3,'y-', bincenters,y4,'o-', bincenters,y5,'p-')'''
        
        title_font = mpl.font_manager.FontProperties(style='italic', weight='bold', size=18)#family='times new roman', 
        label_font = mpl.font_manager.FontProperties(style='italic', size=16)
        xlb = plt.xlabel('Percentile bucket')
        ylb = plt.ylabel('Normalized number of known risky domains')  # normalized means that the sum area under the ORIGINAL histogram BARS is 1, it is not real percentage, cause potentially one bar can be higher than 1 if another is very low...
        title = plt.title('Histogram of the known risky domains\nrisk ranks per algorithm',y=1.005)
        title.set_font_properties(title_font) 
        xlb.set_font_properties(label_font)
        ylb.set_font_properties(label_font)
        #plt.legend(bbox_to_anchor=(0.75, 1.), loc=2, borderaxespad=0.,prop={'size':11})
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=3,prop={'size':11}, fancybox=True, shadow=True)
        
        
        '''ax = plt.subplot(111)  
        ax.spines["top"].set_visible(False)  
        ax.spines["bottom"].set_visible(False)  
        ax.spines["right"].set_visible(False)  
        ax.spines["left"].set_visible(False)  
        
        ax.get_xaxis().tick_bottom()  
        ax.get_yaxis().tick_left()'''
        ylim = list(plt.axis())[-2:]
        for y in np.arange(ylim[0], ylim[1], 0.005):  
            plt.plot(range(0,10), [y] * 10, "--", lw=0.5, color="black", alpha=0.3)  
        
        plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                        labelbottom="on", left="off", right="off", labelleft="on")  

        
        #plt.show()
        plt.savefig(''.join([fn,'.png']))
        return

    
    def export_info(self,fn,raw_flag=False):
        ''' writes the stats object info to file
        Parameters
        ----------
        fn = (string) full path name of output file
        raw_flag = (bool) is True for writing the raw data as well (Lpct values) 
        
        Returns
        -------
        None'''
        import csv
        ordered_atr = [self.atr.min,self.atr.max,self.atr.avg,self.atr.median,self.atr.std,\
                        self.atr.g80,self.atr.g85,self.atr.g90,self.atr.g95,\
                        self.atr.pct_g80,self.atr.pct_g85,self.atr.pct_g90,self.atr.pct_g95,\
                        self.atr.num_of_mal,self.atr.num_of_test_domains,self.atr.auc] 
        f=open(fn, "wb")
        w = csv.writer(f)
        np.set_printoptions(precision=3)    # For printing numpy objects- prints 3 decimal after the point.
        w.writerow(['Algorithm'] + ordered_atr)
        for k,v in self.stats.items():
            w.writerow([k] + ["%.3f"%v[atr] for atr in ordered_atr])
        if raw_flag:    # writing the domains-Lpct dict
            w.writerow([' ']); w.writerow(['Lpct values'])
            w.writerow(['Domain']+sorted(self.stats))
            for d in self.domains_list:
                w.writerow([d]+["%.3f"%v['Lpct_dict'][d] for alg,v in sorted(self.stats.items())])
            
        f.close()
        return
    
       
def stats_union(stats_list,fn,raw_flag=False):
    ''' union several stats objects into one object (and write its info to a file at the end)
        Parameters
        ----------
        stats_list = a list of stats objects
        fn = (string) full path name of output file
        raw_flag = (bool) is True for writing the raw data as well (Lpct values) 
        
        Returns
        -------
        None'''
    if len(stats_list) == 1:    #In cases of NO K fold cross validation (evaluated domains list is empty)
        u_s = stats_list[0]
    else:   #K fold cross validation
        s = stats_list[0]
        u_obj = s.stats
        algs_list = u_obj.keys()
        u_dicts_list = [ u_obj[alg]['Lpct_dict'] for alg in algs_list ]
        u_test_label_list = stats_list[0].test_labels
        u_test_scores_list = [ u_obj[alg]['test_scores_list'] for alg in algs_list ]
        accum_aucs_list = [ u_obj[alg][s.atr.auc]*len(s.test_labels) for alg in algs_list ]
        
        for idx,alg in enumerate(algs_list):   # concatenate all Lpct dicts to the one of first object for each alg (saved as list of those dicts- u_dicts_list)
            for s in stats_list[1:]:    # stats_list[0] already in u_dicts_list
                u_dicts_list[idx].update(s.stats[alg]['Lpct_dict'])  
                u_test_scores_list[idx] = np.concatenate([u_test_scores_list[idx],s.stats[alg]['test_scores_list']])
                accum_aucs_list[idx] += s.stats[alg][s.atr.auc]*len(s.test_labels)
                if not idx: #enter for the first algorithm only- for each object in stats_list
                    u_test_label_list = np.concatenate([u_test_label_list,s.test_labels])
        u_s = stats(algs_list,u_dicts_list,u_test_label_list,u_test_scores_list)
        u_s.calc_stats()
        
        # calc averaged aucs and update u_s accordingly (the auc of the union stats is not correct, cause you cannot compare the Lpct scores of different domains from different runs of the same algorithm, basically it got worse auc values than actual average)
        num_of_domains = len(u_s.test_labels)
        for idx,alg in enumerate(algs_list):
            u_s.stats[alg][u_s.atr.auc] = accum_aucs_list[idx]/num_of_domains
    u_s.export_info(fn,raw_flag)
    u_s.export_seed_histogram(fn=fn[:-4])
    return

'''#FOR DEBUG:
def main():
    import generalMethods as gm
    from datetime import datetime
    s_obj = gm.read_object_from_file(fn='/home/michal/SALSA_files/tmp/s_obj')
    s_obj.export_seed_histogram(fn='/home/michal/SALSA_files/tmp/s_obj_'+datetime.now().strftime("%H:%M:%S"))
    return
main()'''
            