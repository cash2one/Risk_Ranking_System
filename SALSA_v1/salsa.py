#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 5, 2014

@author: User
'''

import networkx as nx
from networkx.exception import NetworkXError
from sklearn.preprocessing import normalize     # For normalizing matrix by row (sums to 1)
import numpy as np
import generalMethods as gm
from datetime import datetime
import sys  #for flush prints

#from networkx.exception import NetworkXError

'''
def add_bipartite_attribute_to_graph(G):
    #This method is for more than one class existence cases
    #so if the graph is conected there is no need in it!
    #bipartite=0 -> means the node is a hub
    #bipartite=1 -> means the node is an authority
    #bipartite=2 -> means the node is both hub and authority.
    
    for n in [node for node,outDegree in G.out_degree().items() if outDegree > 0]:  #For each node which has at least one outgoing link 
        G.node[n]['bipartite']=0
    for n in [node for node,outDegree in G.in_degree().items() if outDegree > 0]:  #For each node which has at least one incoming link
        if 'bipartite' not in G.node[n].keys(
                                             ):     # The node wasn't labeled as a hub
            G.node[n]['bipartite']=1
        else:                                       # The node was already labeled as a hub
            G.node[n]['bipartite']=2
    
    return

def get_list_of_hub_nodes(G):
    #Returns list of hub nodes
    return [n for n,d in G.nodes(data=True) if d['bipartite']==0 or d['bipartite']==2]

def get_list_of_authority_nodes(G):
    #Returns list of authority nodes
    return [n for n,d in G.nodes(data=True) if d['bipartite']==1 or d['bipartite']==2]

'''


def get_matrix_norm_by_row(G,sparse=False):
    """Return the transition matrix normalized by its rows- so each row sums to 1."""
    # L is the transition matrix
    if(sparse==True):
        L=nx.to_scipy_sparse_matrix(G,nodelist=G.nodes())
    else:
        L=nx.to_numpy_matrix(G,nodelist=G.nodes())
    return normalize(L.copy(), axis=1, norm='l1')
    
def get_matrix_norm_by_col(G,sparse=False):
    """Return the transition matrix normalized by its columns- so each column sums to 1."""
    # L is the transition matrix
    if(sparse==True):
        L=nx.to_scipy_sparse_matrix(G,nodelist=G.nodes())
    else:
        L=nx.to_numpy_matrix(G,nodelist=G.nodes())
    return (normalize(L.copy().T, axis=1, norm='l1')).T

def get_matrix(G,mat_type=None,sparse=False, force_ergodicity=False, CN_name='CN'):
    """Return the SALSA authority or hub matrix."""
    print '\t~~~~~~ get_matrix (' + mat_type + ')  ~~~~~~'; sys.stdout.flush()
    #L_r is the transition matrix normalized by columns (each column sums to 1)
    L_r=get_matrix_norm_by_row(G,sparse=sparse)
    
    L_c=get_matrix_norm_by_col(G,sparse=sparse)
    
    if (mat_type=='hub'):
        #DEBUG: H=np.dot(L_r,L_c.T); print('\nH: sum of each row: ' + str(np.sum(H,axis=1)) + '\nH: sum of each column: ' + str(np.sum(H,axis=0)))
        if(sparse==True): M = L_r*L_c.T
        else: M = np.dot(L_r,L_c.T)
    elif (mat_type=='authority'):
        #DEBUG: A=np.dot(L_c.T,L_r); print('\nA: sum of each row: ' + str(np.sum(A,axis=1)) + '\nA: sum of each column: ' + str(np.sum(A,axis=0)))
        if(sparse==True): M = L_c.T*L_r
        else: M = np.dot(L_c.T,L_r)
    else:
        print 'Please specify the matrix type you wish to get! returns nothing'
        return
    
    if force_ergodicity:
        CN_index = G.nodes().index(CN_name)
        M = gm.convert_SL_and_CN_weights_to_val(M, val=gm.epsilon, CN_idx=CN_index, stochastic_out=True)
    return M

def add_noise(G,noise=1e-13):
    # Add noise to the greater weights in the graph
    # NOTE: this method is used to handle the eigs() RuntimeError: Factor is exactly singular
    max_weight = max(e[2]['weight'] for e in G.edges_iter(data=True)) 
    for e in G.edges_iter(data=True):
        if e[2]['weight'] == max_weight:
            e[2]['weight'] += noise
    if not gm.check_if_stochastic_matrix(nx.to_numpy_matrix(G)):
        nx.stochastic_graph(G, copy=False)
    return G
        



def salsa(G,max_iter=100,tol=1.0e-8,nstart_dict=None,normalized=True):
    """Return HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for a node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Parameters
    ----------
    G : graph
      A NetworkX graph

    max_iter : interger, optional
      Maximum number of iterations in power method.

    tol : float, optional
      Error tolerance used to check convergence in power method iteration.

    nstart : dictionary, optional
      Starting value of each node for power method iteration.

    normalized : bool (default=True)
       Normalize results by the sum of all of the values.

    Returns
    -------
    (hubs,authorities) : two-tuple of dictionaries
       Two dictionaries keyed by node containing the hub and authority
       values.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> h,a=nx.hits(G)

    Notes
    -----
    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    The HITS algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Jon Kleinberg,
       Authoritative sources in a hyperlinked environment
       Journal of the ACM 46 (5): 604-32, 1999.
       doi:10.1145/324133.324140.
       http://www.cs.cornell.edu/home/kleinber/auth.pdf.
    """
    print '\n\t~~~~~~ salsa (iterative) ~~~~~\n'
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("salsa() not defined for graphs with multiedges.")
    if len(G) == 0:
        return {},{}
    ''' For more than one class existence cases:
    hNodes=get_list_of_hub_nodes(G)
    aNodes=get_list_of_authority_nodes(G)
    '''
    # choose fixed starting vector if not given
    if nstart_dict is None:
        h=dict.fromkeys(G,1.0/G.number_of_nodes())
        #h=dict.fromkeys(hNodes, 1./len(hNodes))        #For more than one class existence cases
    else:
        h=nstart_dict        # IN MY CASE: is it the init of hubs or authorities??
        ''' For more than one class existence cases:
        h={}
        for n in hNodes:
            h[n]=nstart[n]
        '''
        # normalize starting vector
        s=1.0/sum(h.values())
        for k in h:
            h[k]*=s
    
    i=0
    L_r=get_matrix_norm_by_row(G)
    L_c=get_matrix_norm_by_col(G)
    while True: # power iteration: make up to max_iter iterations
        hlast=h
        h=dict.fromkeys(hlast.keys(),0)
        a=dict.fromkeys(hlast.keys(),0)
        #a=dict.fromkeys(aNodes,0)           #For more than one class existence cases
        
        # this "matrix multiply" looks odd because it is
        # doing a left multiply a^T=hlast^T*G
        for n in h:
            for nbr in G[n]:        #G[n] = all the out links of node n
                #a[nbr]+=hlast[n]*G[n][nbr].get('weight',1)
                a[nbr]+=hlast[n]*L_r[n][nbr]
        # now multiply h=Ga
        for n in h:
            for nbr in G[n]:        #G[n] = all the out links of node n
                #h[n]+=a[nbr]*G[n][nbr].get('weight',1)
                h[n]+=a[nbr]*L_c[n][nbr]                
        # normalize vector
        s=1.0/max(h.values())
        for n in h: h[n]*=s
        # normalize vector
        s=1.0/max(a.values())
        for n in a: a[n]*=s
        # check convergence, l1 norm
        err=sum([abs(h[n]-hlast[n]) for n in h])
        if err < tol:
            print '\nnum of iteration: ' + str(i)
            break
        if i>max_iter:
            #raise NetworkXError("HITS: power iteration failed to converge in %d iterations."%(i+1))
            ''''DEBUG:'''
            print '\n###\tSALSA: power iteration failed to converge in ' + str(i+1) + ' iterations- returns the current vectors'
            break
            
        i+=1
    #DEBUG: print('\nh before norm:' + str(h) + '\na before norm:' + str(a))
    ''' Normalization so the max value equal to 1:
    if normalized:
        s = 1.0/sum(a.values())
        for n in a:
            a[n] *= s
        s = 1.0/sum(h.values())
        for n in h:
            h[n] *= s
    '''
    if normalized:
        s=1./sum(a.values())
        for n in a:
            a[n]*=s
        s=1./sum(h.values())
        for n in h:
            h[n]*=s
    #DEBUG: print('\nh after norm:' + str(h) + '\na after norm:' + str(a))
    #DEBUG- Print output:
    print '\nh after ' + str(i+1) + ' iterations:'; gm.print_dict_ordered_by_value(h); print '\na after ' + str(i+1) + ' iterations:'; gm.print_dict_ordered_by_value(a)
    
    return h,a

def salsa_numpy(G,normalized=True):
    """Return HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for a node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Parameters
    -----------
    G : graph
      A NetworkX graph

    normalized : bool (default=True)
       Normalize results by the sum of all of the values.

    Returns
    -------
    (hubs,authorities) : two-tuple of dictionaries
       Two dictionaries keyed by node containing the hub and authority
       values.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> h,a=nx.hits(G)

    Notes
    -----
    The eigenvector calculation uses NumPy's interface to LAPACK.

    The HITS algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Jon Kleinberg,
       Authoritative sources in a hyperlinked environment
       Journal of the ACM 46 (5): 604-32, 1999.
       doi:10.1145/324133.324140.
       http://www.cs.cornell.edu/home/kleinber/auth.pdf.
    """
    print '\n\t~~~~~~ salsa_numpy (eigenvector calc) ~~~~~~\n'
    try:
        import numpy as np
        import scipy as sp
    except ImportError:
        raise ImportError(\
            "hits_numpy() requires NumPy: http://scipy.org/")
    if len(G) == 0:
        return {},{}
    print '--- salsa_numpy: start time- ' + str(datetime.now())
    startTime = datetime.now()      
    #np.set_printoptions(precision=3)    # For printing numpy objects- prints 3 decimal after the point.
    H_sparse = get_matrix(G,mat_type='hub',sparse=True)
    print '--- salsa_numpy: get_matrix (hub) took: '+str(datetime.now()-startTime); tmpTime = datetime.now()
    eps = gm.epsilon
    # DEBUG:
    new_G_h = nx.DiGraph(H_sparse)
    print 'is new graph strongly connected? ' + str(nx.is_strongly_connected(new_G_h))
    print 'is new graph aperiodic? ' + str(nx.is_aperiodic(new_G_h))
    #H = gm.convert_all_matrix_zeros_to_val(H_sparse, val=eps, stochastic_out=True)
    #print '--- salsa_numpy: convert_all_matrix_zeros_to_eps took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now()
    H = H_sparse.todense() 
    #e,ev=np.linalg.eig(H)
    e,ev=sp.linalg.eig(H,left=True,right=False)
    #e,ev=np.linalg.eig(H.T) #we send H.T for calculating the LEFT eigenvector!
    print '--- salsa_numpy: calculating hub eigs took: ' + str(datetime.now()-tmpTime)
    
    #e,ev=sps.linalg.eigs(H,left=True,right=False)
    m=e.argsort()[-1] # index of maximum eigenvalue
    '''#DEBUG: 
    print('\nH:\n' + str(H.round(3)))
    print'\ne rounded (3)\n' + str(e.round(3)) + '\nev rounded (3)\n' + str(ev.round(3))
    print 'm- index of maximum eigenvalue= ' + str(m) + ',  max eigenvalue= ' + str(e[m]) + \
        '\nev rounded (3)\n' + str(np.array(ev[:,m]).flatten().round(3))'''
    h=np.array(ev[:,m]).flatten()
    # DEBUG:
    print h
    
    tmpTime = datetime.now()
    
    A_sparse = get_matrix(G,mat_type='authority',sparse=True)
    print '--- salsa_numpy: get_matrix (authority) took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now()
    new_G_a = nx.DiGraph(A_sparse)
    print 'is new graph strongly connected? ' + str(nx.is_strongly_connected(new_G_a))
    print 'is new graph aperiodic? ' + str(nx.is_aperiodic(new_G_a))
    #A = gm.convert_all_matrix_zeros_to_val(A_sparse, val=eps, stochastic_out=True)
    #print '--- salsa_numpy: convert_all_matrix_zeros_to_eps took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now()
    A = A_sparse.todense() 
    e,ev=sp.linalg.eig(A,left=True,right=False)
    #e,ev=sps.linalg.eigs(A,left=True,right=False)
    #e,ev=np.linalg.eig(A.T) #we send A.T for calculating the LEFT eigenvector!
    print '--- salsa_numpy: calculating hub eigs took: ' + str(datetime.now()-tmpTime)
    m=e.argsort()[-1] # index of maximum eigenvalue  
    a=np.array(ev[:,m]).flatten()
    '''#DEBUG: 
    print('\n\nA:\n' + str(A.round(3)))
    print 'm- index of maximum eigenvalue= ' + str(m) + '\ne rounded (3)\n' + str(e.round(3)) + '\nev rounded (3)\n' + str(ev.round(3))
    print('\nh before norm:' + str(h) + '\na before norm:' + str(a))
    print 'max eigenvalue= ' + str(e[m]) + '\nev rounded (3)\n' + str(np.array(ev[:,m]).flatten().round(3))'''
    
    if normalized:
        h = h/h.sum()
        a = a/a.sum()
    else:
        h = h/h.max()
        a = a/a.max()
    hubs=dict(zip(G.nodes(),map(float,h)))
    authorities=dict(zip(G.nodes(),map(float,a)))

    return hubs,authorities

def salsa_sparse(G,CN_name='CN',normalized=True, debug_mode=False):
    """Return HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for a node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Parameters
    -----------
    G : graph
      A NetworkX graph

    normalized : bool (default=True)
       Normalize results by the sum of all of the values.

    Returns
    -------
    (hubs,authorities) : two-tuple of dictionaries
       Two dictionaries keyed by node containing the hub and authority
       values.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> h,a=nx.hits(G)

    Notes
    -----
    The eigenvector calculation uses NumPy's interface to LAPACK.

    The HITS algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Jon Kleinberg,
       Authoritative sources in a hyperlinked environment
       Journal of the ACM 46 (5): 604-32, 1999.
       doi:10.1145/324133.324140.
       http://www.cs.cornell.edu/home/kleinber/auth.pdf.
    """
    print '\n\t~~~~~~ salsa_sparse (G, CN_name='+str(CN_name)+', normalized='+str(normalized)+', debug_mode='+str(debug_mode)+') ~~~~~~\n'
    try:
        #import numpy as np
        import scipy as sp
        import sys
    except ImportError:
        raise ImportError(\
            "salsa_sparse() requires SciPy: http://scipy.org/")
    if len(G) == 0:
        return {},{}
    print '--- salsa_sparse: start time- ' + str(datetime.now()); sys.stdout.flush()
    startTime = datetime.now()      
    #np.set_printoptions(precision=3)    # For printing numpy objects- prints 3 decimal after the point.
    print '--- salsa_sparse: hub- percentage of non-zero elements: '+str(float(nx.to_scipy_sparse_matrix(G).getnnz())/G.number_of_nodes()**2); sys.stdout.flush()
    H = get_matrix(G,mat_type='hub',sparse=True)
    print '--- salsa_sparse: get_matrix (hub) took: '+str(datetime.now()-startTime); tmpTime = datetime.now(); sys.stdout.flush()
    print '--- salsa_sparse: hub- percentage of non-zero elements: '+str(float(H.getnnz())/G.number_of_nodes()**2); sys.stdout.flush()
    eps = gm.epsilon
    H = gm.convert_SL_and_CN_weights_to_val(H, val=eps, CN_idx=G.nodes().index(CN_name), stochastic_out=True)
    print '\n--- salsa_sparse: convert_SL_and_CN_weights_to_val took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
    print '--- salsa_sparse: hub- percentage of non-zero elements: '+str(float(H.getnnz())/G.number_of_nodes()**2); sys.stdout.flush()
    
    if debug_mode:
        new_G_h = nx.DiGraph(H)
        print '\n--- salsa_sparse: hub- is new graph stochastic? ' + str(gm.check_if_stochastic_matrix(nx.to_numpy_matrix(new_G_h))); sys.stdout.flush()
        print '--- salsa_sparse: hub- is new graph strongly connected? ' + str(nx.is_strongly_connected(new_G_h)); sys.stdout.flush()
        print '--- salsa_sparse: hub- is new graph aperiodic? ' + str(nx.is_aperiodic(new_G_h)); sys.stdout.flush()
        new_G_h.clear()
        print '--- salsa_sparse: debug steps (hub) took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
        #H = gm.convert_all_matrix_zeros_to_val(H_sparse, val=eps, stochastic_out=True)
        
    e,h = sp.sparse.linalg.eigen.arpack.eigs(H.T, k=1, sigma=1, which='LM')
    print '\n--- salsa_sparse: calculating hub eigs took: ' + str(datetime.now()-tmpTime); sys.stdout.flush()
    tmpTime = datetime.now()
    
    A = get_matrix(G,mat_type='authority',sparse=True)
    print '--- salsa_sparse: get_matrix (authority) took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
    print '--- salsa_sparse: authority- percentage of non-zero elements: '+str(float(A.getnnz())/G.number_of_nodes()**2); sys.stdout.flush()
    A = gm.convert_SL_and_CN_weights_to_val(A, val=eps, CN_idx=G.nodes().index(CN_name), stochastic_out=True)
    print '\n--- salsa_sparse: convert_SL_and_CN_weights_to_val took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
    print '--- salsa_sparse: authority- percentage of non-zero elements: '+str(float(A.getnnz())/G.number_of_nodes()**2); sys.stdout.flush()
    
    if debug_mode:
        new_G_a = nx.DiGraph(A)
        print '\n--- salsa_sparse: hub- is new graph stochastic? ' + str(gm.check_if_stochastic_matrix(nx.to_numpy_matrix(new_G_a))); sys.stdout.flush()
        print '--- salsa_sparse: authority- is new graph strongly connected? ' + str(nx.is_strongly_connected(new_G_a)); sys.stdout.flush()
        print '--- salsa_sparse: authority- is new graph aperiodic? ' + str(nx.is_aperiodic(new_G_a)); sys.stdout.flush()
        new_G_a.clear()
        print '--- salsa_sparse: debug steps (authority) took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
        #A = gm.convert_all_matrix_zeros_to_val(A_sparse, val=eps, stochastic_out=True)
        #print '--- salsa_numpy: convert_all_matrix_zeros_to_eps took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now()
        
    e,a = sp.sparse.linalg.eigen.arpack.eigs(A.T, k=1, sigma=1, which='LM')    
    print '\n--- salsa_sparse: calculating hub eigs took: ' + str(datetime.now()-tmpTime); sys.stdout.flush()
    

    if normalized:
        h = h/h.sum()
        a = a/a.sum()
    else:
        h = h/h.max()
        a = a/a.max()
    
    if (h.imag.sum() != 0. or a.imag.sum() != 0. ):
        print '##### COMPLEX VECTOR!!!! returning the real part only!!! #####'; sys.stdout.flush()

    hubs=dict(zip(G.nodes(),map(float,h.real)))
    authorities=dict(zip(G.nodes(),map(float,a.real)))

    return hubs,authorities

def salsa_per_class(G):
    # G is the original graph
    print '\t~~~~~~ salsa_per_class ~~~~~~'; startTime = datetime.now(); sys.stdout.flush()
    authorities_dict, auth_class_dict = calc_salsa_per_class(G, rank_type='authority')
    hubs_dict, hub_class_dict = calc_salsa_per_class(G, rank_type='hub')
    print '\n\t\t--- salsa_per_class took: '+str(datetime.now()-startTime); sys.stdout.flush()
    return hubs_dict, hub_class_dict, authorities_dict, auth_class_dict

def calc_salsa_per_class(G, rank_type):
    # G is the original graph
    # rank_type = 'authority' or 'hub' 
    import scipy.sparse
    print '\t\t~~~~~~ calc_salsa_per_class ~~~~~~'; startTime = datetime.now(); sys.stdout.flush()

    # Authority:
    A=get_matrix(G,mat_type=rank_type,sparse=True)
    G_new = nx.DiGraph(A)
    '''DEBUG:
    out_file = ''.join(['/home/michal/SALSA_files/tmp/real_run/middle_graph_',str(rank_type)])
    gm.write_graph_to_file(G_new, out_file)'''
    #x=scipy.ones((n,1))/n  # initial guess
    isolates = nx.isolates(G_new)   # isolate node is a node with in_deg=out_deg=0
    print '--- calc_salsa_per_class: num of isolates- '+str(len(isolates))+', out of- '+str(G_new.number_of_nodes())+' nodes ('+str(float(len(isolates))/G_new.number_of_nodes())+'%)'; sys.stdout.flush()
    num_of_not_isolates = G_new.number_of_nodes() - len(isolates)
    scores_dict = {}
    tmpTime = datetime.now()
    classes = nx.strongly_connected_component_subgraphs(G_new)
    print '--- calc_salsa_per_class: separate to classes took- '+str(datetime.now()-tmpTime); sys.stdout.flush(); tmpTime = datetime.now()
    #remove classes of isolated nodes:   
    classes[:] = [ c for idx,c in enumerate(classes) if c.nodes()[0] not in isolates ]
    print '--- calc_salsa_per_class: clean classes from isolates took- '+str(datetime.now()-tmpTime); sys.stdout.flush(); 
    
    num_of_classes = 0
    domain_class_dict = {}
    for subG in classes:
        num_of_classes += 1
        '''DEBUG: 
        out_file = ''.join(['/home/michal/SALSA_files/tmp/real_run/graph_',str(classes.index(subG))])
        gm.write_graph_to_file(subG, out_file)'''
        tmp_d = eig_calc(subG, normalize=num_of_not_isolates)   
        #tmp_d = power_iteration(subG,max_iter=100,tol=1.0e-8,normalize=num_of_not_isolates,nstart=None)
        #tmp_d = power_iteration(subG, normalize=num_of_not_isolates, nstart=[v[G.n_attr.risk] for v in subG.nodes(data=True)])
        for k,v in tmp_d.items():
            d = G.nodes()[k]
            scores_dict[d] = v
            domain_class_dict[d] = num_of_classes
    print '--- calc_salsa_per_class: num of classes (NOT including isolates)- '+str(num_of_classes)
    for i in isolates:
        d = G.nodes()[i]
        scores_dict[d] = 0
        domain_class_dict[d] = 0 # class zero represents the isolates
    #print authority_dict
    print '--- calc_salsa_per_class took: '+str(datetime.now()-startTime); sys.stdout.flush()

    return scores_dict, domain_class_dict

def eig_calc(G,normalize=None):
    import scipy as sp
    #print '\n\t~~~~~~ eig_calc ~~~~~~'; startTime = datetime.now(); sys.stdout.flush()
    startTime = datetime.now() 
    n = G.number_of_nodes()
    if n == 1:
        eigvec = np.array([1])
    elif n == 2:     # for handling ValueError: k must be less than ndim(A)-1, k=1
        return power_iteration(G,normalize=normalize)
    else:    # the graph contains more than 2 nodes
        A=nx.to_scipy_sparse_matrix(G)
        '''print '--- eig_calc: is sub graph stochastic? ' + str(gm.check_if_stochastic_matrix(nx.to_numpy_matrix(G)))#; sys.stdout.flush()
        print '--- eig_calc: is sub graph strongly connected? ' + str(nx.is_strongly_connected(G))#; sys.stdout.flush()
        print '--- eig_calc: is sub graph aperiodic? ' + str(nx.is_aperiodic(G));# sys.stdout.flush()
        print '--- eig_calc: debug step took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
        '''
        try:
            eigval,eigvec = sp.sparse.linalg.eigen.arpack.eigs(A.T, k=1, sigma=1, which='LM')
        except RuntimeError:    
            B=nx.to_scipy_sparse_matrix(add_noise(G))
            eigval,eigvec = sp.sparse.linalg.eigen.arpack.eigs(B.T, k=1, sigma=1, which='LM')
        #eigval,eigvec = sp.sparse.linalg.eigen.arpack.eigs(A.T, k=1, which='LM')
        #print '--- eig_calc: eigs took: '+str(datetime.now()-tmpTime); sys.stdout.flush()
        #print '--- eig_calc: sub graph eigval- '+str(eigval)
    eigvec = eigvec/eigvec.sum()
    if normalize:
        norm_factor = float(n)/normalize
        eigvec = eigvec*norm_factor    
    #if (eigvec.imag.sum() != 0. ):
    #    print '##### COMPLEX VECTOR!!!! returning the real part only!!! #####'; #sys.stdout.flush(
    results_dict = dict(zip(G.nodes(),map(float,eigvec.real)))
    if n > 100: print '--- eig_calc: calc of class contains '+str(n)+' nodes, ('+str(float(n)/normalize)+'% of the non-isolates nodes from the graph) took-'+str(datetime.now()-startTime); sys.stdout.flush()
    return results_dict

def power_iteration(G,max_iter=100,tol=1.0e-8,normalize=None,nstart=None):
    import scipy#.sparse
    #import numpy as np
    startTime = datetime.now() 
    n=nx.number_of_nodes(G)
    A=nx.to_scipy_sparse_matrix(G)
    
    if nstart is None:
        x=(scipy.ones((n,1))/n).T  # initial guess
    else:
        #x=np.asarray(nstart_dict.values()).flatten()       # IN MY CASE: is it the init of hubs or authorities??
        x=np.asarray(nstart)
        # normalize starting vector
        s=1.0/x.sum()
        for k in x:
            x[k]*=s
    # power iteration on authority matrix
    i=0
    while True:
        xlast=x
        x=x*A   # we multiple from left for extracting the matrix row 
        x=x/x.max()
        # check convergence, l1 norm
        err=scipy.absolute(x-xlast).sum()
        if err < tol:
            break
        if i>max_iter:
            # in general- this method is used when there are only 2 nodes in the class 
            # if the graph is aperiodic than the vector we got after max_iter is good eanough
            if nx.is_aperiodic(G):   
                print '(salsa) power_iteration: (APERIODIC CLASS- ',n,' nodes) failed to converge in %d iterations, continues with the last vector!!!'%(i+1)
                break
            else: #the class is periodic
                print '(salsa) power_iteration: (',n,' nodes) PERIODIC CLASS!!!'
                raise NetworkXError("(salsa) power_iteration: (PERIODIC CLASS) power iteration failed to converge in %d iterations."%(i+1))
        i+=1

    results=np.asarray(x).flatten()
    results = results/results.sum()
    if normalize:
        norm_factor = float(G.number_of_nodes())/normalize
        results = results*norm_factor
    results_dict = dict(zip(G.nodes(),map(float,results)))
    if n > 100: print '--- power_iteration: calc of class contains '+str(n)+' nodes, ('+str(float(n)/normalize)+'% of the main graph) took-'+str(datetime.now()-startTime); sys.stdout.flush()
    return results_dict

def salsa_scipy(G,max_iter=100,tol=1.0e-6,normalized=True):
    """Return HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for a node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Parameters
    -----------
    G : graph
      A NetworkX graph

    max_iter : interger, optional
      Maximum number of iterations in power method.

    tol : float, optional
      Error tolerance used to check convergence in power method iteration.

    nstart : dictionary, optional
      Starting value of each node for power method iteration.

    normalized : bool (default=True)
       Normalize results by the sum of all of the values.

    Returns
    -------
    (hubs,authorities) : two-tuple of dictionaries
       Two dictionaries keyed by node containing the hub and authority
       values.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> h,a=nx.hits(G)

    Notes
    -----
    This implementation uses SciPy sparse matrices.

    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    The HITS algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Jon Kleinberg,
       Authoritative sources in a hyperlinked environment
       Journal of the ACM 46 (5): 604-632, 1999.
       doi:10.1145/324133.324140.
       http://www.cs.cornell.edu/home/kleinber/auth.pdf.
    """
    try:
        import scipy#.sparse
        import numpy as np
    except ImportError:
        raise ImportError(\
            "hits_scipy() requires SciPy: http://scipy.org/")
    if len(G) == 0:
        return {},{}
    #M=nx.to_scipy_sparse_matrix(G,nodelist=G.nodes())
    #(n,m)=M.shape # should be square
    #A=M.T*M # authority matrix
    n=nx.number_of_nodes(G)
    A=get_matrix(G,mat_type='authority',sparse=True)
    x=scipy.ones((n,1))/n  # initial guess
    # power iteration on authority matrix
    i=0
    while True:
        xlast=x
        x=A*x   # right eigenvector?! 
        x=x/x.max()
        # check convergence, l1 norm
        err=scipy.absolute(x-xlast).sum()
        if err < tol:
            break
        if i>max_iter:
            raise NetworkXError(\
            "salsa_scipy: power iteration failed to converge in %d iterations."%(i+1))
        i+=1

    a=np.asarray(x).flatten()
    # h=M*a
    M=get_matrix_norm_by_row(G,sparse=True)
    h=np.asarray(M*a).flatten()
    if normalized:
        h = h/h.sum()
        a = a/a.sum()
    hubs=dict(zip(G.nodes(),map(float,h)))
    authorities=dict(zip(G.nodes(),map(float,a)))
    return hubs,authorities

def salsa_scipy_old(G,max_iter=100,tol=1.0e-6,nstart_dict=None,normalized=True, debug=False):
    """Return HITS hubs and authorities values for nodes.

    The HITS algorithm computes two numbers for a node.
    Authorities estimates the node value based on the incoming links.
    Hubs estimates the node value based on outgoing links.

    Parameters
    -----------
    G : graph
      A NetworkX graph

    max_iter : interger, optional
      Maximum number of iterations in power method.

    tol : float, optional
      Error tolerance used to check convergence in power method iteration.

    nstart : dictionary, optional
      Starting value of each node for power method iteration.

    normalized : bool (default=True)
       Normalize results by the sum of all of the values.

    Returns
    -------
    (hubs,authorities) : two-tuple of dictionaries
       Two dictionaries keyed by node containing the hub and authority
       values.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> h,a=nx.hits(G)

    Notes
    -----
    This implementation uses SciPy sparse matrices.

    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    The HITS algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs.

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Jon Kleinberg,
       Authoritative sources in a hyperlinked environment
       Journal of the ACM 46 (5): 604-632, 1999.
       doi:10.1145/324133.324140.
       http://www.cs.cornell.edu/home/kleinber/auth.pdf.
    """
    #import sys
    print '\n\t~~~~~~ salsa_scipy (G, max_iter='+str(max_iter)+', tol='+str(tol)+', nstart_dict, normalized='+str(normalized)+') ~~~~~~\n'; sys.stdout.flush()
    try:
        import scipy#.sparse as sp
        import numpy as np
        import sys
    except ImportError:
        raise ImportError(\
            "hits_scipy() requires SciPy: http://scipy.org/")
    if len(G) == 0:
        return {},{}
    print '--- salsa_scipy: ' + str(datetime.now()); sys.stdout.flush(); startTime = datetime.now()      
    ''''M=nx.to_scipy_sparse_matrix(G,nodelist=G.nodes())
    (n,m)=M.shape # should be square
    A=M.T*M # authority matrix'''
    A=get_matrix(G,mat_type='authority',sparse=True,force_ergodicity=True, CN_name=10)
    (n,m)=A.shape # should be square
    if debug:
        new_G_h = nx.DiGraph(A)
        print '\n--- salsa_scipy_old: hub- is new graph stochastic? ' + str(gm.check_if_stochastic_matrix(nx.to_numpy_matrix(new_G_h))); sys.stdout.flush()
        print '--- salsa_scipy_old: hub- is new graph strongly connected? ' + str(nx.is_strongly_connected(new_G_h)); sys.stdout.flush()
        print '--- salsa_scipy_old: hub- is new graph aperiodic? ' + str(nx.is_aperiodic(new_G_h)); sys.stdout.flush()
        new_G_h.clear()
        #print '--- salsa_scipy_old: debug steps (hub) took: '+str(datetime.now()-tmpTime); tmpTime = datetime.now(); sys.stdout.flush()
        
    
    print '--- salsa_scipy: get authority matrix took: ' + str(datetime.now()-startTime); sys.stdout.flush(); tmpTime = datetime.now()      
    
    # choose fixed starting vector if not given
    if nstart_dict is None:
        a=scipy.ones((n,1))/n  # initial guess
    else:
        a=np.asarray(nstart_dict.values()).flatten()       # IN MY CASE: is it the init of hubs or authorities??
        # normalize starting vector
        s=1.0/a.sum()
        for k in a:
            a[k]*=s
            
    # power iteration on authority matrix
    i=0
    a=a.T
    L_c=get_matrix_norm_by_col(G,sparse=True)
    while True:
        alast=a
        
        #x=M*x
        a=a*A
        a=a/a.max() 
        # check convergence, l1 norm
        err=scipy.absolute(a-alast).sum()
        if err < tol:
            break
        if i>max_iter:
            #raise NetworkXError("HITS: power iteration failed to converge in %d iterations."%(i+1))
            ''''DEBUG:'''
            print '\n###\tSALSA_SCIPY: power iteration failed to converge in ' + str(i+1) + ' iterations- returns the current vectors'
            break
        i+=1
    
    print '--- salsa_scipy: authorities vector calculation took: ' + str(datetime.now()-tmpTime)
    tmpTime = datetime.now()      
    a=np.asarray(a).flatten()
    # h=M*a
    #h=np.asarray(M*a).flatten()
    h=np.asarray(L_c*a.T).flatten()
    #h=np.asarray(L_c*a).flatten()
    print '--- salsa_scipy: hubs vector calculation took: ' + str(datetime.now()-tmpTime)
    tmpTime = datetime.now()  
     
    if normalized:
        h = h/h.sum()
        a = a/a.sum()
    print '--- salsa_scipy: vectors normalization took: ' + str(datetime.now()-tmpTime)
    
    hubs=dict(zip(G.nodes(),map(float,h)))
    authorities=dict(zip(G.nodes(),map(float,a)))
    #DEBUG- Print output: print '\nh after ' + str(i+1) + ' iterations:'; gm.print_dict_ordered_by_value(hubs); print '\na after ' + str(i+1) + ' iterations:'; gm.print_dict_ordered_by_value(authorities)
    print '--- salsa_scipy: all method took: ' + str(datetime.now()-startTime)
    
    return hubs,authorities






