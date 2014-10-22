#!/usr/local/anaconda/bin/python2.7
'''
Created on Dec 26, 2013

@author: michal
'''
import networkx as nx
from networkx.exception import NetworkXError
#__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
#__all__ = ['pagerank','pagerank_numpy','pagerank_scipy','google_matrix']
def stochastic_graph(G, copy=True, weight='weight'):
    """Return a right-stochastic representation of G.

    A right-stochastic graph is a weighted digraph in which all of
    the node (out) neighbors edge weights sum to 1.

    Parameters
    -----------
    G : graph
      A NetworkX graph

    copy : boolean, optional
      If True make a copy of the graph, otherwise modify the original graph

    weight : edge attribute key (optional, default='weight')
      Edge data key used for weight.  If no attribute is found for an edge
      the edge weight is set to 1.
    """
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise nx.NetworkXError('stochastic_graph not implemented '
                               'for multigraphs')

    if not G.is_directed():
        raise nx.NetworkXError('stochastic_graph not implemented '
                               'for undirected graphs')

    if copy:
        W = nx.DiGraph(G)
    else:
        W = G # reference original graph, no copy

    degree = W.out_degree(weight=weight)
    for (u,v,d) in W.edges(data=True):
        if(degree[u]): d[weight] = float(d.get(weight,1.0))/degree[u]
        else: 
            #DEBUG: print ("stochastic_graph: degree is zero "+str(u))
            d[weight] = 0
    return W

def pagerank(G,alpha=0.85,personalization=None,
             max_iter=100,tol=1.0e-8,nstart=None,weight='weight'):
    """Return the PageRank of the nodes in the graph.

    PageRank computes a ranking of the nodes in the graph G based on
    the structure of the incoming links. It was originally designed as
    an algorithm to rank web pages.

    Parameters
    -----------
    G : graph
      A NetworkX graph

    alpha : float, optional
      Damping parameter for PageRank, default=0.85

    personalization: dict, optional
       The "personalization vector" consisting of a dictionary with a
       key for every graph node and nonzero personalization value for each node.

    max_iter : integer, optional
      Maximum number of iterations in power method eigenvalue solver.

    tol : float, optional
      Error tolerance used to check convergence in power method solver.

    nstart : dictionary, optional
      Starting value of PageRank iteration for each node.

    weight : key, optional
      Edge data key to use as weight.  If None weights are set to 1.

    Returns
    -------
    pagerank : dictionary
       Dictionary of nodes with PageRank as value

    Examples
    --------
    >>> G=nx.DiGraph(nx.path_graph(4))
    >>> pr=nx.pagerank(G,alpha=0.9)

    Notes
    -----
    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    The PageRank algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs by converting each oriented edge in the
    directed graph to two edges.

    See Also
    --------
    pagerank_numpy, pagerank_scipy, google_matrix

    References
    ----------
    .. [1] A. Langville and C. Meyer,
       "A survey of eigenvector methods of web information retrieval."
       http://citeseer.ist.psu.edu/713792.html
    .. [2] Page, Lawrence; Brin, Sergey; Motwani, Rajeev and Winograd, Terry,
       The PageRank citation ranking: Bringing order to the Web. 1999
       http://dbpubs.stanford.edu:8090/pub/showDoc.Fulltext?lang=en&doc=1999-66&format=pdf
    """
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("pagerank() not defined for graphs with multiedges.")

    if len(G) == 0:
        return {}

    if not G.is_directed():
        D=G.to_directed()
    else:
        D=G

    # create a copy in (right) stochastic form
    #W=nx.stochastic_graph(D, weight=weight)
    W=stochastic_graph(D, weight=weight)
    scale=1.0/W.number_of_nodes()

    # choose fixed starting vector if not given
    if nstart is None:
        x=dict.fromkeys(W,scale)
    else:
        x=nstart
        # normalize starting vector to 1
        s=1.0/sum(x.values())
        for k in x: x[k]*=s

    # assign uniform personalization/teleportation vector if not given
    if personalization is None:
        p=dict.fromkeys(W,scale)
    else:
        p=personalization
        # normalize starting vector to 1
        s=1.0/sum(p.values())
        for k in p:
            p[k]*=s
        if set(p)!=set(G):
            print "MyPageRank, len of personalization: " + str(len(personalization))
            print "MyPageRank, len of p: " + str(len(p))
            for myKey in set(p):
                if myKey not in set(G): print "not in G:" + myKey + "#end"
            for myKeyG in set(G):
                if myKeyG not in set(p): print "not in p:" + myKeyG + "#end"
            raise NetworkXError('Personalization vector '
                                'must have a value for every node')


    # "dangling" nodes, no links out from them
    out_degree=W.out_degree()
    dangle=[n for n in W if out_degree[n]==0.0]
    i=0
    while True: # power iteration: make up to max_iter iterations
        xlast=x
        x=dict.fromkeys(xlast.keys(),0)
        danglesum=alpha*scale*sum(xlast[n] for n in dangle)
        for n in x:
            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
                x[nbr]+=alpha*xlast[n]*W[n][nbr][weight]
            x[n]+=danglesum+(1.0-alpha)*p[n]
        # normalize vector
        s=1.0/sum(x.values())
        for n in x:
            x[n]*=s
        # check convergence, l1 norm
        err=sum([abs(x[n]-xlast[n]) for n in x])
        if err < tol:
            break
        if i>max_iter:
            raise NetworkXError('pagerank: power iteration failed to converge '
                                'in %d iterations.'%(i-1))
        i+=1
    return x