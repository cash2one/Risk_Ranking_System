#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 24, 2014

@author: michal
'''
import networkx as nx
import salsa
import generalMethods as gm



class edge_attributes():
    good = 'g'
    bad = 'b'
    weight = 'weight'
    
class node_attributes():
    risk = 'risk'                           # the initial risk score of the domain (blackLists)
    
    salsa_hub_score = 'salsa_hub'
    salsa_auth_score = 'salsa_authority'
    salsa_auth_position = 'salsa_auth_pos'
    salsa_hub_position = 'salsa_hub_pos'
    salsa_auth_bucket = 'salsa_auth_bucket'
    salsa_hub_bucket = 'salsa_hub_bucket'
    salsa_auth_u_pct = 'salsa_auth_u_pct'   # authority upper percentile (pct of scores under OR EQUAL to it's score)
    salsa_auth_l_pct = 'salsa_auth_l_pct'   # authority lower percentile (pct of scores under to it's score)
    salsa_hub_u_pct = 'salsa_hub_u_pct'
    salsa_hub_l_pct = 'salsa_hub_l_pct'
    salsa_auth_class = 'salsa_auth_class'   # class 0 = isolates, class 1 = biggest strongly connected class
    salsa_hub_class = 'salsa_hub_class'
    
    hits_hub_score = 'hits_hub'
    hits_auth_score = 'hits_authority'
    hits_hub_bucket = 'hits_hub_bucket'
    hits_auth_bucket = 'hits_auth_bucket'
    hits_auth_u_pct = 'hits_auth_u_pct'
    hits_auth_l_pct = 'hits_auth_l_pct'
    hits_hub_u_pct = 'hits_hub_u_pct'
    hits_hub_l_pct = 'hits_hub_l_pct'
    
    pagerank_score = 'pr'
    pagerank_bucket = 'pr_bucket'
    pagerank_u_pct = 'pr_u_pct'   
    pagerank_l_pct = 'pr_l_pct'
    
    inverse_pagerank_score = 'inv_pr'
    inverse_pagerank_bucket = 'inv_pr_bucket'
    inverse_pagerank_u_pct = 'inv_pr_u_pct'   
    inverse_pagerank_l_pct = 'inv_pr_l_pct'
    
class buckets():
    buckets = {}
    
    def create_domain_bucket_dict(self):
        # create and return dict of each domain and it's bucket (as per the member 'buckets').
        domain_bucket_dict = {}
        for b,v_dict in self.buckets.items():
            for e in v_dict['elements']:
                domain_bucket_dict[e] = b
        return domain_bucket_dict
    
    def update_buckets_keys(self):
        # makes sure the buckets start from zero, if not- shift the keys to start from zero.
        first_bucket = min(self.buckets.keys())
        # force the bucket keys to strat from 0 
        if first_bucket: #first bucket key greater than zero
            for b,v in self.buckets.items():
                self.buckets[b-first_bucket] = self.buckets.pop(b)
        
        return 
    
    def update_buckets_info(self,d):
        for b,v in self.buckets.items():
            if len(v['elements']): # if bucket isn't empty
                v['min_val'] = d[v['elements'][0]]    # update min value
                v['max_val'] = d[v['elements'][-1]]    # update max value
                v['num_of_elements'] = len(v['elements'])
                v['absolut_range'] = v['max_val']-v['min_val']
            else:   # bucket is empty
                v['min_val'] = None
                v['max_val'] = None
                v['num_of_elements'] = 0
                v['absolut_range'] = 0
        
        # add dist_from_prev_bucket (between ech bucket max val and the min val of the prev bucket):     
        #min_bucket = min(self.buckets.keys())
        first_bucket = min(self.buckets.keys())
        for b,v in self.buckets.items():
            #min_val_of_prev_bucket = self.buckets[max(b-1,min_bucket)]['min_val']
            
            if b != first_bucket: # if not first bucket
                if self.buckets[b-1]['num_of_elements'] and v['num_of_elements']:  # if prev or current bucket not empty
                    v['dist_from_prev_bucket'] = self.buckets[b-1]['min_val'] - v['max_val']    # min_val of prev bucket minus max_val of current bucket
                else:   # prev or current bucket are empty
                    v['dist_from_prev_bucket'] = 0
            else: # first bucket 
                v['dist_from_prev_bucket'] = 0
                
        return #buckets
    
    def print_buckets_info(self):
        from operator import itemgetter
        for b, v in sorted(self.buckets.items(), key=itemgetter(0)):
            print 'bucket #' + str(b) +\
            ', num of elements: ' + str(v['num_of_elements']) +\
            ', min val: ' + str(v['min_val']) + \
            ', max val: ' + str(v['max_val']) +\
            ', absolut range: ' + str(v['absolut_range']) +\
            ', dist from prev bucket: ' + str(self.buckets[b]['dist_from_prev_bucket'])
            
            '''for b in buckets:
            print 'bucket #' + str(b) + \
            ', num of elements: ' + str(buckets[b]['num_of_elements']) +\
            ', min val: ' + str(buckets[b]['min_val']) + \
            ', max val: ' + str(buckets[b]['max_val'])
            '''
        
        return
             

class domains_graph():
    G = nx.DiGraph              # directed graph: node = domain, edge(A,B) = user passed from domain A to B
    CN = 'CN'                   # Central Node (first/last domain in each session connected from/to this node) 
    e_attr = edge_attributes()  # edge_attributes instantiation (for coding purposes only)
    n_attr = node_attributes()  # node_attributes instantiation (for coding purposes only)
    #b = buckets()               # buckets instantiation
    # useful dicts for coding
    alg_auth_Lpct = {'salsa':n_attr.salsa_auth_l_pct, \
                     'hits':n_attr.hits_auth_l_pct, \
                     'pagerank':n_attr.pagerank_l_pct,\
                     'inverse_pagerank':n_attr.inverse_pagerank_l_pct}            
    alg_hub_Lpct = {'salsa':n_attr.salsa_hub_l_pct, \
                    'hits':n_attr.hits_hub_l_pct}
    alg_auth_score = {'salsa':n_attr.salsa_auth_score, \
                     'hits':n_attr.hits_auth_score, \
                     'pagerank':n_attr.pagerank_score,\
                     'inverse_pagerank':n_attr.inverse_pagerank_score}            
    alg_hub_score = {'salsa':n_attr.salsa_hub_score, \
                    'hits':n_attr.hits_hub_score}
    
    def __init__(self, transitions_dict_file,domain_risk_dict_path,whiteList_file):
        #G = nx.from_dict_of_dicts(Transitions_Dict, create_using, multigraph_input)
        self.G = nx.DiGraph(gm.readDict(transitions_dict_file)) # graph instantiation
        self.add_nodes_attr(self.n_attr.risk, gm.readDict(domain_risk_dict_path))
        self.whiteList_set = self.create_white_list_for_post_filtering(whiteList_file)  # create/load the whiteList domains (set)
        return
    
    def clear(self):
        self.G.clear()
        
        return
    
    def graph_Preprocessing(self, eps):
        self.fix_no_in_degree(eps)
        self.fix_no_out_degree(eps)
        #self.add_CN_full_conections(eps)
        return

    def fix_no_in_degree(self, eps):
        added_edges_list = []
        no_in_deg_nodes = { k for k,v in self.G.in_degree().items() if not v }
        for k in no_in_deg_nodes:
            added_edges_list.append((self.CN,k,eps))
        self.add_edges(added_edges_list)
        return
    
    def fix_no_out_degree(self, eps):
        added_edges_list = []
        no_out_deg_nodes = { k for k,v in self.G.out_degree().items() if not v }
        for k in no_out_deg_nodes:
            added_edges_list.append((k,self.CN,eps))
        self.add_edges(added_edges_list)
        return
    
    def add_CN_full_conections(self, eps):
        added_edges_list = []
        # link all nodes to CN
        no_CN_incoming_links_nodes = {n for n in self.G.nodes_iter() if not self.G.has_edge(n, self.CN)}
        for n in no_CN_incoming_links_nodes:
            added_edges_list.append((n,self.CN,eps))

        # link CN to all nodes   
        no_CN_outgoing_links_nodes = {n for n in self.G.nodes_iter() if not self.G.has_edge(self.CN, n)}
        for n in no_CN_outgoing_links_nodes:
            added_edges_list.append((self.CN,n,eps))
            
        self.add_edges(added_edges_list)
        return
    
    def add_edges(self, edges_list):
        if edges_list:
            self.G.add_weighted_edges_from(edges_list)
        return
    
    def add_nodes_attr(self,attr_name,attr_val_dict):
        if len(attr_val_dict) == nx.number_of_nodes(self.G):
            nx.set_node_attributes(self.G, name=attr_name, attributes=attr_val_dict)
        else:
            for n in self.G.nodes_iter():
                if n in attr_val_dict:
                    self.G.node[n][attr_name] = attr_val_dict[n]
                else:
                    self.G.node[n][attr_name] = 0
        return
    
    def get_nodes_attr_val_dict(self,attr_name):
        return nx.get_node_attributes(self.G, name=attr_name)
    
    def get_nodes_attr_val_dict_OLD(self,attr_name):
        nodes_attr_dict = dict()
        for n in self.G.nodes_iter():
            nodes_attr_dict[n] = self.G.node[n][attr_name]
        return nodes_attr_dict

    def create_white_list_for_post_filtering(self,fn):
        ''' Creates a file of white list domains (if not already exits) where there was high incoming traffic,
        high means more than the averaged of the number of users entered to domain by all its incoming edges. '''
        import os, math, tldextract
        if not os.path.exists(fn):
            b_domains_set = {}
            '''b_domains_set = {'xhamster.com','adultism.com','dojki.com','mygames.com.ua','bigpoint.com','flashgames.ru',\
                             'a10.com','xnxx.com','nick.de','porngaytube.net','amazingwildtube.com','youporn.com',\
                             'redtube.com','besttubeclips.net','youjizz.com','jacquieetmichel.net','dudesnude.com',\
                             'sourceforge.net','kinox.to','hentai.ms','imagefap.com','movie2k.to','sexuria.com',\
                             'gallerysex.net','ashemaletube.com','xvideos.com','escort-ireland.com','tube8.com',\
                             'perveden.com','gidonline.ru','met-art.com','oddassy.com','cam4.com'}'''
            g_domains_set = {'google','facebook','ebay','twitter','yandex','paypal','citibank','bing','yahoo','youtube',\
                             'apple','tripadvisor'} 
            whiteList_set = {'babylon.com','walla.co.il','flickr.com','netflix.com','firefox.com','conduit.com',\
                             'washingtonpost.com','endomondo.com','linkedin.com','avg.com','ask.com','reddit.com'}  # set var not dict.
            
            added_whiteList = [d for d in self.G.nodes_iter() if tldextract.extract(d).domain in g_domains_set]
            whiteList_set.update(added_whiteList)   # insert the new domains from added_whiteList (list) to the whiteList_set (set)
            del added_whiteList[:]  # clear added_whiteList
            
            
            g_traffic_dict = self.G.in_degree(weight=self.e_attr.good)
            #gm.write_dict_ordered_by_value_to_file(g_traffic_dict, '_'.join([fn,'DEBUG_goodTraffic']))
            avg = math.ceil(float(sum(g_traffic_dict.values()))/len(g_traffic_dict))
            trh = 10 * avg
            added_whiteList = [k for k,v in g_traffic_dict.items() if v>=trh]
            print 'create_white_list_for_post_filtering: avg=',avg,' , trh=',trh,' , added_whiteList before cleaning: len=',len(added_whiteList)#,' , added_whiteList=',added_whiteList
            # Delete known risky domains from the whiteList:
            added_whiteList[:] = [d for d in added_whiteList if self.G.node[d][self.n_attr.risk] < gm.risk_threshold and d not in b_domains_set] # remove from the good users popular domains the ones which known as risky (from blacklists) or known as porn/problematic domains (b_domains_set)
            print 'create_white_list_for_post_filtering: added_whiteList AFTER cleaning: len=',len(added_whiteList)#,' , added_whiteList=',added_whiteList
            whiteList_set.update(added_whiteList)   # insert the new domains from added_whiteList (list) to the whiteList_set (set)                   
            
            # for DEBUG:
            self.export_traffic_info_DEBUG('_'.join([fn,'DEBUG_traffic_info']))
            WL_dict = dict((k,v) for k,v in g_traffic_dict.items() if k in added_whiteList)
            gm.write_dict_ordered_by_value_to_file(WL_dict, '_'.join([fn,'DEBUG'])) # mainly for debug!! 
            # end DEBUG
            
            '''white_flag_dict = {d:0 for d in self.G.nodes_iter()}    # init dict of all nodes with value zero     
            for d in whiteList_set: white_flag_dict[d] = 1          # changes the domains exist in whiteList_set to 1 in the white_flag_dict 
            gm.write_object_to_file(white_flag_dict, fn)  # write the whiteList to using pickle for later loading
            '''
        else: 
            whiteList_set = gm.read_object_from_file(fn)
            
        #self.add_nodes_attr(self.n_attr.is_white, white_flag_dict)
        return whiteList_set
    
    def post_filtering_results(self,alg):
        for d in self.whiteList_set:
            if d in self.G.nodes(): self.G.node[d][self.alg_auth_score[alg]] = 0.0
        if alg in self.alg_hub_score:
            for d in self.whiteList_set:
                if d in self.G.nodes(): self.G.node[d][self.alg_hub_score[alg]] = 0.0
        return
    
    
    def run_hits(self,hits_type='hits_scipy', max_iter=100, tol=1e-08, nstart=None, normalized=True):
        '''# IMPORTANT: the forced ergodicity is made on the graph itself and not on it's copy!!!!
        self.add_CN_full_conections(eps=gm.epsilon)
        nx.stochastic_graph(self.G, copy=False)
        if debug_mode:
            import sys
            print '\n--- run_hits: is new graph stochastic? ' + str(gm.check_if_stochastic_matrix(nx.to_numpy_matrix(self.G))); sys.stdout.flush()
            print '--- run_hits: is new graph strongly connected? ' + str(nx.is_strongly_connected(self.G)); sys.stdout.flush()
            print '--- run_hits: is new graph aperiodic? ' + str(nx.is_aperiodic(self.G)); sys.stdout.flush()
            #print '--- run_hits: debug steps (hub) took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
        '''    
        run = {'hits_scipy':'nx.hits_scipy(self.G, max_iter, tol, normalized)', \
               'hits_numpy':'nx.hits_numpy(self.G, normalized)', \
               'hits':'nx.hits(self.G, max_iter, tol, nstart, normalized)'}
        
        try:
            h,a = eval(run[hits_type])
        except:   
            try:
                #hits_type = 'hits'
                print '\t@@@ HITS: trying increasing max iterations!'
                max_iter *= 100 
                h,a = eval(run[hits_type])
            except: 
                print '\t@@@ HITS: max iterations still not working- returns empty dicts!!! '
                h = a = {}
        
        self.add_nodes_attr(self.n_attr.hits_hub_score, h)
        self.add_nodes_attr(self.n_attr.hits_auth_score, a)
        return h,a

    def run_pagerank(self,inverse=False, pagerank_type='pagerank_scipy', alpha=0.85, personalization=None, max_iter=100, tol=1e-06, weight='weight',nstart=None):
        if inverse: # if inverse pagerank (backwards direction)
            #  IMPORTANT: reverse the graph itself and not it's copy!!!!!
            self.G.reverse(copy=False)
            attr_name = self.n_attr.inverse_pagerank_score
        else:   # 'regular' pagerank (forwards direction)
            attr_name = self.n_attr.pagerank_score
        
        run = {'pagerank_scipy':'nx.pagerank_scipy(self.G, alpha, personalization, max_iter, tol, weight)', \
               'pagerank_numpy':'nx.pagerank_numpy(self.G, alpha, personalization, weight)', \
               'pagerank':'nx.pagerank(self.G,alpha, personalization, max_iter, tol, nstart, weight)'}
        PR = eval(run[pagerank_type])
        self.add_nodes_attr(attr_name, PR)
        return None,PR  # the first is None- cause when calling this method we assume there might be hubs scores as well...
       
    def run_salsa(self,salsa_type='salsa_per_class', normalized=True, nstart=None, tol=10e-8, max_iter=1000, nstart_flag=False):
        run = {'iterative':'salsa.salsa(self.G, max_iter, tol, nstart, normalized)', \
               'eigenvector':'salsa.salsa_numpy(self.G, normalized)', \
               'sparse_eigenvector':'salsa.salsa_sparse(self.G,normalized=True)',\
               'sparse_iterrative':'salsa.salsa_scipy(self.G, max_iter, tol, normalized)',\
               'salsa_per_class':'salsa.salsa_per_class(self.G, nstart_flag=nstart_flag)'}  #'sparse_iterrative':'salsa.salsa_scipy(self.G, max_iter, tol, nstart, normalized)'}
        h, h_classes, a, a_classes = eval(run[salsa_type])
        self.add_nodes_attr(self.n_attr.salsa_hub_score, h)
        self.add_nodes_attr(self.n_attr.salsa_auth_score, a)
        self.add_nodes_attr(self.n_attr.salsa_hub_class, h_classes)
        self.add_nodes_attr(self.n_attr.salsa_auth_class, a_classes)
        return h,a
    
    
    
    def evaluate_hubs_and_authorities_algorithems(self,auth_fn,hub_fn,alg_type='salsa'):
        #divide all nodes to (20?) buckets (by auth score) and return how many malwares exist in each bucket
        #other possible way is (when there is no convergance) remove one of the malware from nstart and then check in 
        #    each bucket it fell
        #other way- compare buckets of pairwise of malware and legit (like ends with .edu/.org)     

        if alg_type == 'salsa':
            auth_score = self.n_attr.salsa_auth_score
            hub_score = self.n_attr.salsa_hub_score
            #node_auth_bucket_attr = self.n_attr.salsa_auth_bucket
            #node_hub_bucket_attr = self.n_attr.salsa_hub_bucket
            auth_u_pct = self.n_attr.salsa_auth_u_pct
            auth_l_pct = self.n_attr.salsa_auth_l_pct
            hub_u_pct = self.n_attr.salsa_hub_u_pct
            hub_l_pct = self.n_attr.salsa_hub_l_pct
            auth_class = self.n_attr.salsa_auth_class
            hub_class = self.n_attr.salsa_hub_class
            
        else:   # HITS (alg_type == 'hits')
            auth_score = self.n_attr.hits_auth_score
            hub_score = self.n_attr.hits_hub_score
            #node_auth_bucket_attr = self.n_attr.hits_auth_bucket
            #node_hub_bucket_attr = self.n_attr.hits_hub_bucket
            auth_u_pct = self.n_attr.hits_auth_u_pct
            auth_l_pct = self.n_attr.hits_auth_l_pct
            hub_u_pct = self.n_attr.hits_hub_u_pct
            hub_l_pct = self.n_attr.hits_hub_l_pct
            auth_class = None
            hub_class = None
            
        self.score_evaluation(auth_score,auth_u_pct,auth_l_pct,auth_fn,auth_class)
        self.score_evaluation(hub_score,hub_u_pct,hub_l_pct,hub_fn,hub_class)
        return
    
    def evaluate_single_score_algorithms(self,fn,alg_type='pagerank'):
        #divide all nodes to (20?) buckets (by auth score) and return how many malwares exist in each bucket
        #other possible way is (when there is no convergance) remove one of the malware from nstart and then check in 
        #    each bucket it fell
        #other way- compare buckets of pairwise of malware and legit (like ends with .edu/.org)     
 
        if alg_type == 'pagerank':
            score_attr = self.n_attr.pagerank_score
            #node_bucket_attr = self.n_attr.pagerank_bucket
            u_pct_attr = self.n_attr.pagerank_u_pct
            l_pct_attr = self.n_attr.pagerank_l_pct
        else: #inverse pagerank
            score_attr = self.n_attr.inverse_pagerank_score
            #node_bucket_attr = self.n_attr.inverse_pagerank_bucket
            u_pct_attr = self.n_attr.inverse_pagerank_u_pct
            l_pct_attr = self.n_attr.inverse_pagerank_l_pct
        self.score_evaluation(score_attr,u_pct_attr,l_pct_attr,fn)
        return
    
    #def score_evaluation(self,node_score_attr_name,node_bucket_attr_name,node_u_pct_attr_name,node_l_pct_attr_name,fn,num_of_buckets=20):
    def score_evaluation(self,score_attr,u_pct_attr,l_pct_attr,fn,class_attr=None):    
        init_risk_dict = self.get_nodes_attr_val_dict(self.n_attr.risk) 
        scores_dict = self.get_nodes_attr_val_dict(score_attr)
        
        u_pct_dict, l_pct_dict = gm.get_percentiles(scores_dict)
        self.add_nodes_attr(u_pct_attr, u_pct_dict)
        self.add_nodes_attr(l_pct_attr, l_pct_dict)
        if class_attr: # SALSA evaluation!
            class_dict = self.get_nodes_attr_val_dict(class_attr)
            gm.write_union_of_dicts_ordered_by_value_to_file(scores_dict, [u_pct_dict,l_pct_dict,class_dict,init_risk_dict], fn)
        else:   # not SALSA 
            gm.write_union_of_dicts_ordered_by_value_to_file(scores_dict, [u_pct_dict,l_pct_dict,init_risk_dict], fn)
        
        '''self.split_to_buckets(scores_dict, num_of_buckets, node_bucket_attr_name)
        #b = buckets(d=scores_dict, num_of_buckets,bucket_attr_name=node_bucket_attr_name)
        buckets_dict = self.get_nodes_attr_val_dict(node_bucket_attr_name)
        gm.write_union_of_dicts_ordered_by_value_to_file(scores_dict, buckets_dict, init_risk_dict, fn)'''
        return

    def evaluate_algorithem(self,auth_fn,hub_fn=None,alg_type='salsa'):
        #divide all nodes to (20?) buckets (by auth score) and return how many malwares exist in each bucket
        #other possible way is (when there is no convergance) remove one of the malware from nstart and then check in 
        #    each bucket it fell
        #other way- compare buckets of pairwise of malware and legit (like ends with .edu/.org)
        
        #print all nodes authority scores and thier init risk rank
        #hubs_file = '/home/michal/SALSA_files/outputs/hubs.csv'
        
        run = {'salsa':'self.evaluate_hubs_and_authorities_algorithems(auth_fn,hub_fn,alg_type=\'salsa\')',\
               'hits':'self.evaluate_hubs_and_authorities_algorithems(auth_fn,hub_fn,alg_type=\'hits\')',\
               'pagerank':'self.evaluate_single_score_algorithms(auth_fn,alg_type=\'pagerank\')',\
               'inverse_pagerank':'self.evaluate_single_score_algorithms(auth_fn,alg_type=\'inverse_pagerank\')'}
        
        eval(run[alg_type])

        return
    
    def alg_histogram(self,alg):
        score_attr_name = {'salsa':'self.n_attr.salsa_auth_score',\
                           'hits':'self.n_attr.hits_auth_score',\
                           'pagerank':'self.n_attr.pagerank_score',\
                           'inverse_pagerank':'self.n_attr.inverse_pagerank_score'}
        self.score_histogram(eval(score_attr_name[alg]))
    
    def score_histogram(self,score_attr):
        gm.histogram_of_dict(self.get_nodes_attr_val_dict(score_attr), bins=self.G.number_of_nodes()/100)
        return
    

    def create_combined_scores(self,run_mode,alg_list=[],evaluated_domain_list=None,attr='Lpct'):
        # alg_list = list of algorithms to combine its scores
        # attr = (string) the node attribute which the combined score is based on
        dicts = []
        if attr == 'Lpct':
            ''' MOVED TO BE A MEMBER!!!
            alg_auth_attr = {'salsa':self.n_attr.salsa_auth_l_pct, \
               'hits':self.n_attr.hits_auth_l_pct, \
               'pagerank':self.n_attr.pagerank_l_pct,\
               'inverse_pagerank':self.n_attr.inverse_pagerank_l_pct}
            
            alg_hub_attr = {'salsa':self.n_attr.salsa_hub_l_pct, \
               'hits':self.n_attr.hits_hub_l_pct}'''
                
            for alg in alg_list:
                dicts.append(self.get_nodes_attr_val_dict(self.alg_auth_Lpct[alg]))#attr[alg]))   # create a dict of the domains l_pct and push it to dicts list
            dicts.append(self.get_nodes_attr_val_dict(self.n_attr.risk))   
        
        for comb_type in ['max','avg','top3_avg','top2_avg']:
            out_file = gm.get_general_file_path(run_mode,'_'.join([comb_type,attr]),evaluated_domain_list,dir='outputs')
            gm.create_combined_score(comb_type,dicts,is_last_dict_risk=True,fn=out_file)   
        
        # create a new high level score for hits and salsa (max of auth/hub score):
        tmp_dicts = []
        for k,v in self.alg_hub_Lpct.items():#attr.items():    # for each alg [salsa, hits]
            tmp_dicts.append( dicts.pop( alg_list.index(k) ) )  # add auth scores dict
            tmp_dicts.append( self.get_nodes_attr_val_dict(v) )
            out_file = gm.get_general_file_path(run_mode,'_'.join([k,'max',attr]),evaluated_domain_list,dir='outputs')
            gm.create_combined_score('max',tmp_dicts,is_last_dict_risk=False,fn=out_file)   
            del tmp_dicts[:]
        
        '''combine_types = {'max_Lpct': 'gm.create_max_dict_from_dicts(dicts)',\
                       'avg_Lpct': 'gm.create_avg_dict_from_dicts(dicts)',\
                       'top3_avg_Lpct': 'gm.create_avg_dict_from_dicts(dicts,n=3)',\
                       'top2_avg_Lpct': 'gm.create_avg_dict_from_dicts(dicts,n=2)'}
        
        for k,v in combine_types.items():        
            out_file = gm.get_general_file_path(run_mode,k,evaluated_domain_list,dir='outputs') 
            comb_score_dict = eval(v)
            u_pct_dict, l_pct_dict = gm.get_percentiles(comb_score_dict)
            gm.write_union_of_dicts_ordered_by_value_to_file(comb_score_dict, [u_pct_dict,l_pct_dict,dicts[-1]], out_file)
        
        # create a new high level score for hits and salsa (max of auth/hub score):
        del dicts[:]
        if attr == 'l_pct':
            alg_hub_attr = {'salsa':self.n_attr.salsa_hub_l_pct, \
               'hits':self.n_attr.hits_hub_l_pct}
            for k,v in alg_hub_attr.items():    # for each alg [salsa, hits]
                dicts.append(self.get_nodes_attr_val_dict(v))                   # add hub scores dict
                dicts.append(self.get_nodes_attr_val_dict(alg_auth_attr[k]))    # add auth scores dict
                out_file = gm.get_general_file_path(run_mode,'_'.join([k,'max']),evaluated_domain_list,dir='outputs')
                comb_score_dict = gm.create_max_dict_from_dicts(dicts)
                u_pct_dict, l_pct_dict = gm.get_percentiles(comb_score_dict)
                gm.write_union_of_dicts_ordered_by_value_to_file(comb_score_dict, [u_pct_dict,l_pct_dict,dicts[-1]], out_file)
        '''        
        
        return


    
    '''def get_nodes_position_dict_from_scores_dict(self,d):
        # d = dict of nodes and its scores (of one of the algorithems- SALSA/HITS/PageRank)
        from operator import itemgetter
        position_dict = {}
        i = 1
        for k in sorted(d.items(), key=itemgetter(1), reverse=True):
            #actual position: position_dict[k] = i
            #percentage position:
            position_dict[k[0]] = float(i)/float(self.G.number_of_nodes())
            i+=1
        return position_dict
    
    def split_to_buckets(self, d, num_of_buckets, bucket_attr_name=None):
        # d = dict of the attribute values for splitting (like aut/hub scores)
        # bucket_attr_name = if you wish to update (e.g.) salsa_auth_bucket of each node.
        # returns: a dict of the buckets and their domains
        from operator import itemgetter
        #print '\n\t~~~~~~ split_to_buckets(num_of_buckets='+str(num_of_buckets)+', d, bucket_attr_name='+bucket_attr_name+') ~~~~~~\n'
        print '\n\t~~~~~~ split_to_buckets(d, num_of_buckets='+str(num_of_buckets)+', bucket_attr_name='+bucket_attr_name+') ~~~~~~\n'
        
        if bucket_attr_name:
            domain_bucket_dict = {}
            
        sorted_d = sorted(d.items(), key=itemgetter(1))

        #buckets = {}
        #b = buckets()   # buckets instantiation
        buckets = self.b.buckets
        buckets.clear()
        
        cur_bucket = num_of_buckets-1
        bucket_capacity = 1.0/num_of_buckets
        bucket_threshold = bucket_capacity
        buckets.setdefault(cur_bucket,{}).setdefault('elements',[])    #init for the first (lowest scores) bucket
        cum_sum = 0
        
        for k,v in sorted_d:
            cum_sum += v
            
            if cur_bucket:      #if this is not the last bucket (where the highest scores are)
                if cum_sum < bucket_threshold:
                    buckets[cur_bucket]['elements'].append(k)
                else:   # new bucket
                    cur_bucket -= 1
                    bucket_threshold += bucket_capacity
                    buckets.setdefault(cur_bucket,{}).setdefault('elements',[k])    #init new bucket
            else:   #last bucket- highest scores
                buckets[cur_bucket]['elements'].append(k)
                
        self.b.update_buckets_keys()    # force the buckets to start from 0 (if not already)        
        # update buckets with general info:
        self.b.update_buckets_info(d)
        self.b.print_buckets_info()
        
        if bucket_attr_name:
            domain_bucket_dict = self.b.create_domain_bucket_dict()
            self.add_nodes_attr(attr_name=bucket_attr_name, attr_val_dict=domain_bucket_dict)
 
        return #buckets '''
       
    def evaluation(self,algs_list,test=[],fn=None):
        import stats
        import numpy as np
        from datetime import datetime
        
        eval_algs_list = []
        Lpct_dicts_list = []
        if not len(test):    # test_mal is empty
            trh = gm.risk_threshold
            '''risk = self.get_nodes_attr_val_dict(self.n_attr.risk)'''
            risk = gm.get_labels_dict_from_dict(d=self.get_nodes_attr_val_dict(self.n_attr.risk), threshold=trh)
            test_mal = [ k for k,v in risk.items() if v == 1 ]
            test = zip(*risk.items())
            '''tmp = np.asarray([0] * len(risk))
            tmp[np.where(np.asarray(test[1])==1)] = 1
            test[1] = tmp
            #test[0] = np.asarray(test[0])'''
             
        else:
            test_mal = test[0][np.where(test[1]==1)]
        test_scores_list = []
        for alg in algs_list:
            Lpct_dicts_list.append(dict((k,self.G.node[k][self.alg_auth_Lpct[alg]]) for k in test_mal)) #dict of the Lpct values of the risky domains ONLY! (the ones with label 1)
            test_scores_list.append([ self.G.node[k][self.alg_auth_Lpct[alg]] for k in test[0] ])   #list of the Lpct values of ALL domains 
            eval_algs_list.append('_'.join([alg,'auth']))
            if alg in self.alg_hub_Lpct:    #hits or salsa
                Lpct_dicts_list.append(dict((k,self.G.node[k][self.alg_hub_Lpct[alg]]) for k in test_mal))  #dict of the Lpct values of the risky domains ONLY! (the ones with label 1)
                test_scores_list.append([ self.G.node[k][self.alg_hub_Lpct[alg]] for k in test[0] ])    #list of the Lpct values of ALL domains 
                eval_algs_list.append('_'.join([alg,'hub']))
        s = stats.stats(eval_algs_list,Lpct_dicts_list,test[1],test_scores_list) # stats instantiation
        s.calc_stats()
        if fn: # "full run" 
            s.export_info(fn=fn,raw_flag=True)
            s.export_seed_histogram(fn=fn[:-4])
        '''#FOR DEBUG:
        else: # a fold run- we still want to export the histogram of the known bad domains:
            s.export_seed_histogram(fn='/home/michal/SALSA_files/outputs/real_run/hist_'+datetime.now().strftime("%H:%M:%S"))'''

            
        
        # Export to weka file:
        #self.export_to_weka_file(algs_list,test)
        
        return s
    
    def export_to_weka_file(self,algs_list,test,fn_train,fn_test,fn_matrix=None):
        import ml
        
        eval_algs_list = []
        Lpct_dicts_list = []
        for alg in algs_list:
            Lpct_dicts_list.append(self.get_nodes_attr_val_dict(self.alg_auth_Lpct[alg]))
            eval_algs_list.append('_'.join([alg,'auth']))
            if alg in self.alg_hub_Lpct:    #hits or salsa
                Lpct_dicts_list.append(self.get_nodes_attr_val_dict(self.alg_hub_Lpct[alg]))
                eval_algs_list.append('_'.join([alg,'hub']))
        trh = gm.risk_threshold
        labels = gm.get_labels_dict_from_dict(d=self.get_nodes_attr_val_dict(self.n_attr.risk), threshold=trh)
        #DEBUG: print self.get_nodes_attr_val_dict(self.n_attr.risk)
        #DEBUG: print labels
        '''for k,v in labels.items():
            if v != 1:
                labels[k] = 0'''
        
        obj = ml.LR(eval_algs_list,Lpct_dicts_list,labels,test)
        obj.export_to_weka_file(fn_train, fn_test)
        if fn_matrix: obj.export_matrix(fn_matrix)
        return
    
    def export_domains_for_strat_Kfolds_forMalOnly(self,dir):
        d = {d:0 for d in self.G.nodes_iter()}#dict(zip(self.G.nodes(),[0]*self.G.number_of_nodes()))
        for k,v in self.get_nodes_attr_val_dict(self.n_attr.risk).items():
            if v == 1: d[k] = 1
        gm.write_object_to_file(d,'/'.join([dir,'domains_risk.csv']))
        
        mal_d = [k for k,v in d.items() if v]
        gm.write_list_to_file(mal_d,'/'.join([dir,'src_mal_domains.csv']))
        
        return
    
    def export_domains_for_strat_Kfolds(self,dir):
        ''' writes 2 files: (1) dict of domain-binary_label in a pickle format, 
                            (2) list of risky domains (the ones labeled as 1)
        Parameters
        ----------
        dir - string, entire path of the output directory (tmp/runMode/mal_d) 
        
        Returns
        -------
        None
        '''
        trh = gm.risk_threshold
        d = gm.get_labels_dict_from_dict(d=self.get_nodes_attr_val_dict(self.n_attr.risk), threshold=trh)
        
        gm.write_object_to_file(d,'/'.join([dir,'domains_risk.csv']))
        
        risky_d = [k for k,v in d.items() if v]
        gm.write_list_to_file(risky_d,'/'.join([dir,'src_mal_domains.csv']))
        
        return
    
    def export_traffic_info_DEBUG(self,fn):
        g_in = self.G.in_degree(weight=self.e_attr.good)
        b_in = self.G.in_degree(weight=self.e_attr.bad)
        g_out = self.G.out_degree(weight=self.e_attr.good)
        b_out = self.G.out_degree(weight=self.e_attr.bad)
        risk = self.get_nodes_attr_val_dict(self.n_attr.risk)
        gm.write_union_of_dicts_ordered_by_value_to_file(d=g_in,dicts_list=[b_in,g_out,b_out,risk],fn=fn)
        return
