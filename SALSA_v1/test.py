#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 17, 2014

@author: michal
'''

import salsa 
import networkx as nx
import numpy as np
import generalMethods as gm
import scipy as sp
import sys
from sklearn.utils.arpack import eigs
from sklearn.utils.arpack import eigsh



#from datetime import datetime
#import graph
#import DEBUG_func as DEBUG

#import matplotlib.pyplot as plt                 # For the graph plot

# Building the graph: (Multigraph is undirected so it won't be useful in my case cause L is the DIRECTED adjacency matrix
'''
G=nx.DiGraph()
NodeList=['g1','g2','g3','g4','g5','g6','g7',\
          'b1','b2','b3','b4']
G.add_nodes_from(NodeList)
e=0.01  #the weight of edge with zero bad activity percentage.
#EdgesSet=[(From_node,To_node,Edge_weight)]
EdgesSet=[('g1','g2',{'weight':0.36}),('g1','g6',{'weight':e}),\
          ('g2','g1',{'weight':e}),('g2','g4',{'weight':1}),('g2','g3',{'weight':e}),('g2','g5',{'weight':0.5}),('g2','b1',{'weight':1}),\
          ('g3','g1',{'weight':e}),('g3','g4',{'weight':0.36}),('g3','g7',{'weight':e}),\
          ('g4','g1',{'weight':0.5}),('g4','g2',{'weight':e}),('g4','g3',{'weight':e}),\
          ('g6','g5',{'weight':e}),\
          ('b1','b2',{'weight':1}),('b1','b3',{'weight':1}),\
          ('b2','b1',{'weight':1}),('b2','b3',{'weight':1}),('b2','g4',{'weight':1}),('b2','g3',{'weight':1}),\
          ('b3','g3',{'weight':1}),('b3','b4',{'weight':1}),('b3','b2',{'weight':1})]
G.add_edges_from(EdgesSet)
'''
def create_transition_matrix_for_testing(graph_type=None, self_link=True, seed_creation=False):
    e=gm.epsilon
    g=e*10
    seed=None
    
    if(self_link==True):    #for aperiodicity
        s=e
        if(graph_type=='article_with_CN'):   #Toy-graph with 3 (0,1,2) CentralNodes with self links: 
            Transition_Matrix=np.matrix([[s,e,e,0,e,0,0,0,0], \
                                         [e,s,e,e,0,0,0,0,0], \
                                         [e,e,s,0,0,0,0,0,e], \
                                         [0,0,0,s,0,1,0,1,0], \
                                         [0,0,0,1,s,0,0,0,0], \
                                         [0,e,0,0,0,s,0,1,0], \
                                         [e,0,0,0,0,0,s,0,0], \
                                         [0,e,0,0,0,1,1,s,0], \
                                         [0,0,0,0,0,0,0,1,s]])
            if(seed_creation==True):
                seed={0: 0, 1: 0, 2: 0, 3: 0.1, 4: 1., 5: 1., 6: 0.5, 7: 0.4, 8: 0.2}
        
        elif(graph_type=='17_nodes_with_SL_no_zeros'):  #Graph with self links and no zeros (for faster convergence)
            #                            [0,    1,    2,    3,    4,    5,    6,    7,    8,    9,    10,    11,    12,    13,    14,    15,    16]
            Transition_Matrix=np.matrix([[s,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    s,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    e,    s,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    s,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    s,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    s,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    s,    g,    e,    e,    e,    e,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    s,    1,    e,    g,    g,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    g,    s,  1/3,    e,    g,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,    g,    s,    e,  1/2,    1,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,  1/2,    e,    s,    e,    e,    e,    e,    1,    1], \
                                         [e,    e,    e,    e,    e,    e,    e,  1/2,    e,    e,    1,    s,    e,    e,    e,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    s,    1,    e,    1,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,    e,    1,    e,    e,    e,    s,    1,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    s,    e,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    1,    e,    s,    e], \
                                         [e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    e,    s]])
            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:1., 14:0, 15:0, 16:0}

        elif(graph_type=='11_nodes_with_one_CN_and_SL'):  #Graph with self links and one root CN-#10 (instead of 7)                  
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9,    10]
            Transition_Matrix=np.matrix([[s,    g,    0,    0,     0,     0,     0,     0,     0,     0,     0], \
                                         [0,    s,    1,    0,     g,     g,     0,     0,     0,     0,     e], \
                                         [0,    g,    s,  1/3,     0,     g,     0,     0,     0,     0,     0], \
                                         [0,    0,    g,    s,     0,   1/2,     1,     0,     0,     0,     e], \
                                         [0,    0,  1/2,    0,     s,     0,     0,     0,     0,     1,     0], \
                                         [0,  1/2,    0,    0,     1,     s,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     s,     1,     0,     1,     0], \
                                         [0,    0,    0,    1,     0,     0,     0,     s,     1,     0,     0], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     s,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     s,     e], \
                                         [e,    0,    e,    e,     e,     e,     0,     0,     0,     0,     s]])

            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0, 10:0}
                
        elif(graph_type=='11_nodes_with_SL_and_one_full_connected_CN'):  #Graph with self links and one root CN-#10 (instead of 7)                  
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9,    10]
            Transition_Matrix=np.matrix([[s,    g,    0,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    s,    1,    0,     g,     g,     0,     0,     0,     0,     e], \
                                         [0,    g,    s,  1/3,     0,     g,     0,     0,     0,     0,     e], \
                                         [0,    0,    g,    s,     0,   1/2,     1,     0,     0,     0,     e], \
                                         [0,    0,  1/2,    0,     s,     0,     0,     0,     0,     1,     e], \
                                         [0,  1/2,    0,    0,     1,     s,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     s,     1,     0,     1,     e], \
                                         [0,    0,    0,    1,     0,     0,     0,     s,     1,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     s,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     s,     e], \
                                         [e,    e,    e,    e,     e,     e,     e,     e,     e,     e,     s]])

            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0, 10:0}
        
        elif(graph_type=='11_nodes_with_SL_and_one_CN_diagonal'):  #Graph with no self links and one CN only-#10 (instead of 6 CNs + 1 root CN):
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9,    10]
            Transition_Matrix=np.matrix([[s,    g,    e,    e,     e,     e,     e,     e,     e,     e,     e], \
                                         [0,    s,    1,    e,     g,     g,     e,     e,     e,     e,     e], \
                                         [0,    g,    s,  1/3,     e,     g,     e,     e,     e,     e,     e], \
                                         [0,    0,    g,    s,     e,   1/2,     1,     e,     e,     e,     e], \
                                         [0,    0,  1/2,    0,     s,     e,     e,     e,     e,     1,     e], \
                                         [0,  1/2,    0,    0,     1,     s,     e,     e,     e,     e,     e], \
                                         [0,    0,    0,    0,     0,     0,     s,     1,     e,     1,     e], \
                                         [0,    0,    0,    1,     0,     0,     0,     s,     1,     e,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     s,     e,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     s,     e], \
                                         [e,    e,    e,    e,     e,     e,     e,     e,     e,     e,     s]])

            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0, 10:0}
                
        else:   #Graph with self links  ('17_nodes_with_CL'):                       
            #                            [0,    1,    2,    3,    4,    5,    6,    7,    8,    9,    10,    11,    12,    13,    14,    15,    16]
            Transition_Matrix=np.matrix([[ s,   0,    0,    0,    0,    0,    e,    0,    0,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    s,    0,    0,    0,    0,    0,    0,    e,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    s,    0,    0,    0,    0,    0,    0,    e,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    s,    0,    0,    0,    0,    0,    0,     e,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    s,    0,    0,    0,    0,    e,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    s,    0,    0,    0,    0,     0,     e,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    s,    g,    0,    0,     0,     0,     0,     0,     0,     0,     0], \
                                         [0,    e,    0,    0,    0,    0,    0,    s,    1,    0,     g,     g,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    g,    s,  1/3,     0,     g,     0,     0,     0,     0,     0], \
                                         [e,    0,    0,    0,    0,    0,    0,    0,    g,    s,     0,   1/2,     1,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,  1/2,    0,     s,     0,     0,     0,     0,     1,     0], \
                                         [0,    0,    0,    e,    e,    0,    0,  1/2,    0,    0,     1,     s,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    0,     0,     0,     s,     1,     0,     1,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    1,     0,     0,     0,     s,     1,     0,     0], \
                                         [0,    0,    e,    0,    0,    0,    0,    0,    0,    0,     0,     0,     0,     0,     s,     0,     0], \
                                         [0,    0,    0,    0,    0,    e,    0,    0,    0,    0,     0,     0,     0,     1,     0,     s,     0], \
                                         [e,    e,    e,    e,    e,    e,    0,    0,    0,    0,     0,     0,     0,     0,     0,     0,     s]])
            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:1., 14:0, 15:0, 16:0}

    else:       #self_link==False
        if(graph_type=='4_nodes_test'):
            Transition_Matrix=np.matrix([[e,1,1,e], \
                                         [1,e,e,1], \
                                         [e,1,e,e], \
                                         [e,1,e,e]])
        elif(graph_type=='article'):    #Toy-graph with no CentralNodes: 
            Transition_Matrix=np.matrix([[0,0,1.,0,1.,0], \
                                         [1.,0,0,0,0,0], \
                                         [0,0,0,0,1.,0], \
                                         [0,0,0,0,0,0], \
                                         [0,0,1.,1.,0,0], \
                                         [0,0,0,0,1.,0]])
        elif(graph_type=='article_with_CN'):  #Toy-graph with 3 (0,1,2) CentralNodes: 
            Transition_Matrix=np.matrix([[0,e,e,0,e,0,0,0,0], \
                                         [e,0,e,e,0,0,0,0,0], \
                                         [e,e,0,0,0,0,0,0,e], \
                                         [0,0,0,0,0,1,0,1,0], \
                                         [0,0,0,1,0,0,0,0,0], \
                                         [0,e,0,0,0,0,0,1,0], \
                                         [e,0,0,0,0,0,0,0,0], \
                                         [0,e,0,0,0,1,1,0,0], \
                                         [0,0,0,0,0,0,0,1,0]])
            if(seed_creation==True):
                seed={0: 0, 1: 0, 2: 0, 3: 0.1, 4: 1., 5: 1., 6: 0.5, 7: 0.4, 8: 0.2}
        
        elif(graph_type=='17_nodes_with_CNs'):  #Graph with no self links:
            #                            [0,    1,    2,    3,    4,    5,    6,    7,    8,    9,    10,    11,    12,    13,    14,    15,    16]
            Transition_Matrix=np.matrix([[0,    0,    0,    0,    0,    0,    e,    0,    0,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    e,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    e,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    0,     e,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    e,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    0,     0,     e,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,    0,    0,    0,    g,    0,    0,     0,     0,     0,     0,     0,     0,     0], \
                                         [0,    e,    0,    0,    0,    0,    0,    0,    1,    0,     g,     g,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    g,    0,  1/3,     0,     g,     0,     0,     0,     0,     0], \
                                         [e,    0,    0,    0,    0,    0,    0,    0,    g,    0,     0,   1/2,     1,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,  1/2,    0,     0,     0,     0,     0,     0,     1,     0], \
                                         [0,    0,    0,    e,    e,    0,    0,  1/2,    0,    0,     1,     0,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    0,     0,     0,     0,     1,     0,     1,     0], \
                                         [0,    0,    0,    0,    0,    0,    0,    0,    0,    1,     0,     0,     0,     0,     1,     0,     0], \
                                         [0,    0,    e,    0,    0,    0,    0,    0,    0,    0,     0,     0,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,    0,    e,    0,    0,    0,    0,     0,     0,     0,     1,     0,     0,     0], \
                                         [e,    e,    e,    e,    e,    e,    0,    0,    0,    0,     0,     0,     0,     0,     0,     0,     0]])

            if(seed_creation==True):
                #nstart_test={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:1., 7:1., 8:1., 9:1., 10:1., 11:1., 12:1., 13:1., 14:1., 15:1., 16:0}
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:1., 14:0, 15:0, 16:0}
        
        elif(graph_type=='11_nodes_with_one_CN'):  #Graph with no self links and one CN only-#10 (instead of 6 CNs + 1 root CN):
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9,    10]
            Transition_Matrix=np.matrix([[0,    g,    0,    0,     0,     0,     0,     0,     0,     0,     0], \
                                         [0,    0,    1,    0,     g,     g,     0,     0,     0,     0,     e], \
                                         [0,    g,    0,  1/3,     0,     g,     0,     0,     0,     0,     0], \
                                         [0,    0,    g,    0,     0,   1/2,     1,     0,     0,     0,     e], \
                                         [0,    0,  1/2,    0,     0,     0,     0,     0,     0,     1,     0], \
                                         [0,  1/2,    0,    0,     1,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     1,     0], \
                                         [0,    0,    0,    1,     0,     0,     0,     0,     1,     0,     0], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     0,     e], \
                                         [e,    0,    e,    e,     e,     e,     0,     0,     0,     0,     0]])

            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0, 10:0}
                
        elif(graph_type=='11_nodes_with_one_CN_connected_to_all_nodes'):  #Graph with no self links and one CN only-#10 (instead of 6 CNs + 1 root CN):
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9,    10]
            Transition_Matrix=np.matrix([[0,    g,    0,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    1,    0,     g,     g,     0,     0,     0,     0,     e], \
                                         [0,    g,    0,  1/3,     0,     g,     0,     0,     0,     0,     e], \
                                         [0,    0,    g,    0,     0,   1/2,     1,     0,     0,     0,     e], \
                                         [0,    0,  1/2,    0,     0,     0,     0,     0,     0,     1,     e], \
                                         [0,  1/2,    0,    0,     1,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     1,     e], \
                                         [0,    0,    0,    1,     0,     0,     0,     0,     1,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     0,     0,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     0,     e], \
                                         [e,    e,    e,    e,     e,     e,     e,     e,     e,     e,     e]])

            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0, 10:0}
                
        elif(graph_type=='11_nodes_with_one_CN_diagonal'):  #Graph with no self links and one CN only-#10 (instead of 6 CNs + 1 root CN):
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9,    10]
            Transition_Matrix=np.matrix([[0,    g,    e,    e,     e,     e,     e,     e,     e,     e,     e], \
                                         [0,    0,    1,    e,     g,     g,     e,     e,     e,     e,     e], \
                                         [0,    g,    0,  1/3,     e,     g,     e,     e,     e,     e,     e], \
                                         [0,    0,    g,    0,     e,   1/2,     1,     e,     e,     e,     e], \
                                         [0,    0,  1/2,    0,     0,     e,     e,     e,     e,     1,     e], \
                                         [0,  1/2,    0,    0,     1,     0,     e,     e,     e,     e,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     e,     1,     e], \
                                         [0,    0,    0,    1,     0,     0,     0,     0,     1,     e,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     0,     e,     e], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     0,     e], \
                                         [e,    0,    e,    e,     e,     e,     0,     0,     0,     0,     0]])

            if(seed_creation==True):
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0, 10:0}

        else:  #Graph with no self links and no CN (so instead 17 nodes there are only 10 nodes):
            #                            [0,    1,    2,    3,     4,     5,     6,     7,     8,     9]
            Transition_Matrix=np.matrix([[0,    g,    0,    0,     0,     0,     0,     0,     0,     0], \
                                         [0,    0,    1,    0,     g,     g,     0,     0,     0,     0], \
                                         [0,    g,    0,  1/3,     0,     g,     0,     0,     0,     0], \
                                         [0,    0,    g,    0,     0,   1/2,     1,     0,     0,     0], \
                                         [0,    0,  1/2,    0,     0,     0,     0,     0,     0,     1], \
                                         [0,  1/2,    0,    0,     1,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     1], \
                                         [0,    0,    0,    1,     0,     0,     0,     0,     1,     0], \
                                         [0,    0,    0,    0,     0,     0,     0,     0,     0,     0], \
                                         [0,    0,    0,    0,     0,     0,     0,     1,     0,     0]])

            if(seed_creation==True):
                #nstart_test={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:1., 7:1., 8:1., 9:1., 10:1., 11:1., 12:1., 13:1., 14:1., 15:1., 16:0}
                seed={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0, 9:0}
    return Transition_Matrix,seed



#Transition_Matrix,nstart=create_transition_matrix_for_testing(graph_type='17_nodes_with_SL_no_zeros', self_link=True, seed_creation=True)
#Transition_Matrix,nstart=create_transition_matrix_for_testing(graph_type='4_nodes_test', self_link=False, seed_creation=False)

#DEBUG (plot of the graph): plt.show(); nx.draw(G); plt.savefig("C:\Users\User\workspace\SALSA")

#hubs,authorities = salsa.salsa_numpy(G,normalized=True)
#print '\nhubs:'; gm.print_dict_ordered_by_value(hubs); print '\nauthorities:'; gm.print_dict_ordered_by_value(authorities)

def test_eig_methods():
    eps = gm.epsilon
    
    # ERGODIC initial matrix:
    print '/t~~~ 11_nodes_with_one_CN_and_SL ~~~'
    Transition_Matrix_ergodic,nstart=create_transition_matrix_for_testing(graph_type='11_nodes_with_one_CN_and_SL', self_link=True, seed_creation=False)
    G=nx.DiGraph(Transition_Matrix_ergodic)
    print nx.strongly_connected_components(G); print nx.is_strongly_connected(G); print nx.is_aperiodic(G)
    M=salsa.get_matrix(G, mat_type='hub', sparse=True)
    G_ = nx.DiGraph(M)
    print nx.strongly_connected_components(G_); print nx.is_strongly_connected(G_); print nx.is_aperiodic(G_)
    print 'num of non-zero elements: ' + str(M.getnnz())
    print '11 nodes with one CN and SL after get_matrix , before the eps filling: is stochastic- '+str(gm.check_if_stochastic_matrix(M.todense()))
    
    #L = gm.convert_all_matrix_zeros_to_val(M, val=eps, stochastic_out=True) #is_sparse=True, 
    L=M.todense()
    #print 'num of non-zero elements after filling: ' + str(np.count_nonzero(L))
    Lden = L.copy().T
    #print 'all Matrix elements are positiv: ' + str((Lden > 0).all())
    
    e1,ev1=sp.linalg.eig(L,left=True,right=False)
    m=e1.argsort()[-1]
    evMax1=np.array(ev1[:,m]).flatten()
    #print '\n\tnp.linalg.eig(left)\n' + str(e1[m]) + '\n' +  str(evMax1)
    print '\n\tsp.linalg.eig(Lden,left=True,right=False)\n' + str(round(e1[m],3)) + '\n' +  str(gm.l1_norm_vector(evMax1).round(3))
    #print '\nall eigval:\n'+str(e1.round(3))+'\n\nall eigvec:\n'+str(ev1.round(3))
      
    
    # NOT ERGODIC initial matrix (with root CN but no Self Links):
    print '\n\t~~~ 11_nodes_with_one_CN ~~~~'
    Transition_Matrix_CN_no_SL,nstart2=create_transition_matrix_for_testing(graph_type='11_nodes_with_one_CN', self_link=False, seed_creation=False)
    G2=nx.DiGraph(Transition_Matrix_CN_no_SL)
    print nx.strongly_connected_components(G2); print nx.is_strongly_connected(G2); print nx.is_aperiodic(G2)
    M2=salsa.get_matrix(G2, mat_type='hub', sparse=True)
    G2_ = nx.DiGraph(M2)
    print nx.strongly_connected_components(G2_); print nx.is_strongly_connected(G2_); print nx.is_aperiodic(G2_)
    print 'num of non-zero elements: ' + str(M2.getnnz())
    print '11 nodes with one CN after get_matrix , before the eps filling: is stochastic- '+str(gm.check_if_stochastic_matrix(M2.todense()))
    #print '/n11 nodes with one CN after get , before the eps filling: \n'+str(M2.todense())
    
    #L2 = gm.convert_all_matrix_zeros_to_val(M2, val=eps, stochastic_out=True) #is_sparse=True,
    #print 'num of non-zero elements after filling: ' + str(np.count_nonzero(L2))
    L2 = M2.todense() 
    Lden2 = L2.copy().T
    
    e_np,ev_np=np.linalg.eig(Lden2)
    m=e_np.argsort()[-1]
    evMax_np=np.array(ev_np[:,m]).flatten()
    #print '\n\tnp.linalg.eig(left)\n' + str(e_np[m]) + '\n' +  str(evMax_np)
    print '\n\tnp.linalg.eig(left)\n' + str(round(e_np[m],3)) + '\n' +  str(gm.l1_norm_vector(evMax_np).round(3))
    
    ''' # NSTART:
    e_eigs,ev_eigs= eigs(M.copy().T, k=1, which='LM', v0=nstart_list, tol=0.001)  #eigs(L.T, k=1, which='LM', v0=nstart_list, tol=0.0001)
    print '\n\teigs(M.T, k=1, which=LM)\n' + str(e_eigs.round(3)) + '\n' +  str(ev_eigs.round(3))
    '''
    
    ''' # SPARSE:
    e,ev=sp.sparse.linalg.eigen.arpack.eigs(M.copy().T, k=1, which='LM')#left=True,right=False)
    m=e.argsort()[-1]
    evMax=np.array(ev[:,m]).flatten()
    print '\n\tsp.sparse.linalg.eigen.arpack.eigs(left, k=1, which=LM)\n' + str(round(e[m],3)) + '\n' + str(evMax.round(3)) 
    '''
    return

def test_scipy_sparse_eigs(G, CN_name, self_link=False, seed_creation=False):
    eps = gm.epsilon
    print 'percentage of non-zero elements: '+str(float(np.count_nonzero(Transition_Matrix))/G.number_of_nodes()**2)
    print 'is strongly connected? '+str(nx.is_strongly_connected(G))+'\nis aperiodic? '+str(nx.is_aperiodic(G))
    M = salsa.get_matrix(G, mat_type='hub', sparse=True)  
    
    CN_index = G.nodes().index(CN_name)
    M = gm.convert_SL_and_CN_weights_to_val(M, val=eps, CN_idx=CN_index, stochastic_out=True)
    new_G = nx.DiGraph(M)  
    
    print 'AFTER get matrix:\npercentage of non-zero elements: ' + str(float(M.getnnz())/G.number_of_nodes()**2)
    print 'is strongly connected? '+str(nx.is_strongly_connected(new_G))+'\nis aperiodic? '+str(nx.is_aperiodic(new_G))
    print 'is stochastic? '+str(gm.check_if_stochastic_matrix(M.todense()))
    print M
    print M.shape[0]
    #M_pow = np.linalg.matrix_power(M.todense(), 111)
    #print M_pow
    e,ev=sp.sparse.linalg.eigen.arpack.eigs(M.copy().T, k=1,sigma=1, which='LM')#, maxiter=100000)
    h = ev/ev.sum()
    print e; print h;
    if (h.imag.sum() != 0.):
        print '##### COMPLEX VECTOR!!!! #####'
    print map(float,h.real)
    '''e1,ev1=sp.linalg.eig(M.todense(),left=True,right=False)
    m=e1.argsort()[-1]
    evMax1=np.array(ev1[:,m]).flatten()
    print '\n\tnp.linalg.eig(left)\n' + str(e1[m]) + '\n' +  str(evMax1)
    '''
    return
    
def sparse_csenario(graph_type, CN_name, self_link=False, seed_creation=False):
    eps = gm.epsilon
    
    print '\t~~~ '+str(graph_type)+' ~~~'
    Transition_Matrix,nstart=create_transition_matrix_for_testing(graph_type, self_link, seed_creation)
    G = nx.DiGraph(Transition_Matrix)
    #test_scipy_sparse_eigs(G, CN_name, self_link, seed_creation)
    #print '\n\n\t~~~~~ salsa_sparse ~~~~~'
    #print salsa.salsa_sparse(G, CN_name=CN_name, normalized=True, debug_mode=True)
    ''''h,a=salsa.salsa_sparse(G, CN_name=CN_name, normalized=True, debug_mode=True)
    print 'salsa_sparse\nh:'; gm.print_dict_ordered_by_value(h)
    print '\na:'; gm.print_dict_ordered_by_value(a)'''
    
    '''#h,a=salsa.salsa_scipy_old(G, debug=True)    #, max_iter, tol, normalized)
    h,a=salsa.salsa_scipy(G)#, debug=True)    #, max_iter, tol, normalized)
    print 'salsa_scipy\nh:'; gm.print_dict_ordered_by_value(h)
    print '\na:'; gm.print_dict_ordered_by_value(a)'''
    
    h,a = salsa.salsa_per_class(G)
    print h
    print a
    
    ''''h,a=nx.hits_scipy(G)
    print 'hits_scipy\nh:'; gm.print_dict_ordered_by_value(h)
    print '\na:'; gm.print_dict_ordered_by_value(a)'''

    return



def test_sparse_eig_methods():
    
    sparse_csenario(graph_type='article', CN_name=10, self_link=False, seed_creation=False)
    #sparse_csenario(graph_type='11_nodes_with_one_CN_and_SL', CN_name=10, self_link=True, seed_creation=False)
    #sparse_csenario(graph_type='11_nodes_with_one_CN_connected_to_all_nodes', CN_name=10, self_link=False, seed_creation=False)
    return

def test_networkx_methods():
    reducible_G = nx.DiGraph(np.matrix([[1,0],[0,1]]))
    print 'reducible- is strongly connected? ' + str(nx.is_strongly_connected(reducible_G)) #False
    print 'reducible- strongly connected components: ' + str(nx.strongly_connected_components(reducible_G)) #[[0], [1]]
    print 'reducible- is aperiodic? ' + str(nx.is_aperiodic(reducible_G)) #True
    
    irreducible_periodic_G = nx.DiGraph(np.matrix([[0,1],[1,0]]))
    print '\nirreducible_periodic- is strongly connected? ' + str(nx.is_strongly_connected(irreducible_periodic_G)) #True
    print 'irreducible_periodic- strongly connected components: ' + str(nx.strongly_connected_components(irreducible_periodic_G)) #[[0, 1]]
    print 'irreducible_periodic- is aperiodic? ' + str(nx.is_aperiodic(irreducible_periodic_G)) #False (2)
    
    ergodic_G = nx.DiGraph(np.matrix([[0,1,1,0],[1,0,0,1],[0,1,0,0],[0,1,0,0]]))
    modified_G = nx.DiGraph(salsa.get_matrix(ergodic_G, mat_type='hub', sparse=False))
    print 'modified- is strongly connected? ' + str(nx.is_strongly_connected(modified_G)) #False
    print 'modified- strongly connected components: ' + str(nx.strongly_connected_components(modified_G)) #[[0, 2, 3], [1]]
    print 'modified- is aperiodic? ' + str(nx.is_aperiodic(modified_G)) #True

    return

def test_eig_error():
    #graph_file = '/home/michal/SALSA_files/tmp/real_run/graph_11'
    #G = gm.read_graph_from_file(graph_file)
    graph_list = [(354, 354, {'weight': 0.5}),\
                  (354, 13291, {'weight': 0.25}),\
                  (354, 11354, {'weight': 0.25}),\
                  (15204, 15204, {'weight': 0.5}),\
                  (15204, 14639, {'weight': 0.5}),\
                  (11210, 6898, {'weight': 0.25}),\
                  (11210, 11210, {'weight': 0.5}),\
                  (11210, 11354, {'weight': 0.25}),\
                  (13291, 354, {'weight': 0.5}),\
                  (13291, 13291, {'weight': 0.5}),\
                  (14639, 13236, {'weight': 0.16666666666666666}),\
                  (14639, 6898, {'weight': 0.16666666666666666}),\
                  (14639, 15204, {'weight': 0.25}),\
                  (14639, 14639, {'weight': 0.41666666666666663}),\
                  (6898, 6898, {'weight': 0.6111111111111112}),\
                  (6898, 13236, {'weight': 0.1111111111111111}),\
                  (6898, 11210, {'weight': 0.16666666666666666}),\
                  (6898, 14639, {'weight': 0.1111111111111111}),\
                  (13236, 6898, {'weight': 0.3333333333333333}),\
                  (13236, 13236, {'weight': 0.3333333333333333}),\
                  (13236, 14639, {'weight': 0.3333333333333333}),\
                  (11354, 11210, {'weight': 0.25}),\
                  (11354, 354, {'weight': 0.25}),\
                  (11354, 11354, {'weight': 0.5})]
    #(11354, 11354, {'weight': 0.5})]

    G = nx.DiGraph(graph_list)
    #print G.edges(data=True)
    print '--- eig_calc: is sub graph stochastic? ' + str(gm.check_if_stochastic_matrix(nx.to_numpy_matrix(G)))#; sys.stdout.flush()
    print '--- eig_calc: is sub graph strongly connected? ' + str(nx.is_strongly_connected(G))#; sys.stdout.flush()
    print '--- eig_calc: is sub graph aperiodic? ' + str(nx.is_aperiodic(G));# sys.stdout.flush()
    #np_mat = nx.to_numpy_matrix(G)
    #print 'det= '+ str(np.linalg.det(np_mat))
    print salsa.eig_calc(G)
    '''try:
        print salsa.eig_calc(G)
    except RuntimeError: 
        max_weight = max(e[2]['weight'] for e in G.edges_iter(data=True))
        noise = 1e-13
        for e in G.edges_iter(data=True):
            if e[2]['weight'] == max_weight:
                e[2]['weight'] += noise
        if not gm.check_if_stochastic_matrix(nx.to_numpy_matrix(G)):
            nx.stochastic_graph(G, copy=False)
        print salsa.eig_calc(G)'''
    
    

    
    return

def test_2_nodes_graph_error():
    graph_file = '/home/michal/SALSA_files/tmp/real_run/auth_g/graph_180'
    G = gm.read_graph_from_file(graph_file)
    print 'num of nodes: '+str(G.number_of_nodes()); sys.stdout.flush()
    print 'edges: '+str(G.edges(data=True)); sys.stdout.flush()
    print salsa.eig_calc(G); sys.stdout.flush()
    M= nx.to_numpy_matrix(G)
    print np.linalg.matrix_power(M, n=20); sys.stdout.flush()
    return

def test_dim_error():
    import sys
    authority_dict={}
    graph_file = '/home/michal/SALSA_files/tmp/real_run/middle_graph_authority'
    G_new = gm.read_graph_from_file(graph_file)
    isolates = nx.isolates(G_new)
    print 'num of isolates: '+str(len(isolates)); sys.stdout.flush()
    num_of_not_isolates = G_new.number_of_nodes() - len(isolates)
    authority_dict = {}
    classes = nx.strongly_connected_component_subgraphs(G_new)
    print 'num of classes including isolates: '+str(len(classes)); sys.stdout.flush()
    #remove classes of isolated nodes:   
    classes[:] = [ c for idx,c in enumerate(classes) if c.nodes()[0] not in isolates ]
    
    print 'num of classes NOT including isolates: '+str(len(classes)); sys.stdout.flush()
    for subG in classes:
        #print type(subG)
        out_file = ''.join(['/home/michal/SALSA_files/tmp/real_run/graph_',str(classes.index(subG))])
        gm.write_graph_to_file(subG, out_file)
        tmp_d = salsa.eig_calc(subG, normalize=num_of_not_isolates)    #power_iteration(subG)
    '''    
        for k,v in tmp_d.items():
            authority_dict[G.nodes()[k]] = v
        #print power_iteration(subG, tol=1.0e-10)
    for i in isolates:
        authority_dict[G.nodes()[i]] = 0
    #print authority_dict
    print '\n--- calc_salsa_per_class took: '+str(datetime.now()-startTime); sys.stdout.flush()'''
    return


def plotting_fine_tuning():
    aFile = '/home/michal/SALSA_files/tmp/real_run/salsa_a_dict_pickle'
    hFile = '/home/michal/SALSA_files/tmp/real_run/salsa_h_dict_pickle'
    a = gm.read_object_from_file(aFile)
    h = gm.read_object_from_file(hFile)
    gm.saveDict('/home/michal/SALSA_files/tmp/real_run/salsa_a_dict', a)
    gm.saveDict('/home/michal/SALSA_files/tmp/real_run/salsa_h_dict', h)
    print max(a.values())
    gm.histogram_of_dict(a)
    return

def test_stats():
    import stats as st
    alg_list = ['alg1','alg2','alg3']
    algs_dicts_list = [{'D1':0,'D2':32.1,'D3':97.43},\
                       {'D1':98.09,'D2':85.3,'D3':17.53},\
                       {'D1':45.6,'D2':59.1,'D3':0}]
    s = st.stats(alg_list,algs_dicts_list)
    s.calc_stats()
    s.export_info(fn='/home/michal/SALSA_files/tmp/small_test/test',raw_flag=True)
    algs_dicts_list_2 = [{'D10':0,'D20':32.1,'D30':97.43},\
                         {'D10':98.09,'D20':85.3,'D30':17.53},\
                         {'D10':45.6,'D20':59.1,'D30':0}]
    s2 = st.stats(alg_list,algs_dicts_list_2)
    #alldicts = reduce(set.union, map(set, map(dict.items, algs_dicts_list_2)))
    st.stats_union([s,s2], fn='/home/michal/SALSA_files/tmp/small_test/test', raw_flag=True)
    return


def create_digraph():
    dod= {0: {1:{'weight':1,'g':2,'b':2}, 2:{'weight':1,'g':3,'b':3}},\
          1: {2:{'weight':1,'g':1,'b':1}}} # single edge (0,1)
    G=nx.DiGraph(dod)
    return  G

def test_agg_in_deg_attrs():
    import math
    dod= {0: {1:{'weight':1,'g':3,'b':2}, 2:{'weight':1,'g':4,'b':3}},\
          1: {2:{'weight':2,'g':1,'b':1}}} # single edge (0,1)
    G=nx.DiGraph(dod)
    g_traffic_dict = G.in_degree(weight='g')
    print g_traffic_dict
    avg = math.ceil(float(sum(g_traffic_dict.values()))/len(g_traffic_dict))
    print [k for k,v in g_traffic_dict.items() if v>=avg]
    
    #nodes = [d for d in G.nodes_iter()]
    #print 'nodes-',nodes
    g_domain_set = {1,3,5}
    for k,v in G.nodes_iter(data=True):
        v['weight'] = 0
    print G.nodes(data=True)

    zero_dict = {d:0 for d in G.nodes_iter()} 
    print 'zero_dict: ',zero_dict
    
    for k,v in G.nodes_iter(data=True):
        if k in g_domain_set: v['weight'] = 100
    print G.nodes(data=True)
    

def main():
    #fn = '/home/michal/SALSA_files/test_matrix'
    #gm.writeMatrixToFile(fn, Lden)
    
    #test_2_nodes_graph_error()
    #test_dim_error()
    #test_eig_error()
    #test_sparse_eig_methods()
    #test_sparse_eig_methods()
    #test_eig_methods()
    #test_networkx_methods()
    #plotting_fine_tuning()
    #test_stats()
    test_agg_in_deg_attrs()
    return

main()
