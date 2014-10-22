#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 28, 2014

@author: michal
'''
#import networkx as nx
def print_num_of_nodes_with_in_deg_greater_than_2(G):
    count = 0
    for n in G.nodes():
        if G.in_degree(n) > 2:
            count += 1
            #print 'node: ' + n + ', in_degree: ' + str(G.in_degree(n))
    print '\nnum of nodes with in degree greater than 2: ' + str(count)        
    return

def print_num_of_nodes_with_in_deg_0(G):
    count = 0
    for n in G.nodes():
        if not G.in_degree(n):
            count += 1
            #print 'node: ' + n + ', in_degree: ' + str(G.in_degree(n))
    print 'num of nodes with in degree equal to zero: ' + str(count)        
    return

def print_num_of_nodes_with_out_deg_0(G):
    count = 0
    for n in G.nodes():
        if not G.out_degree(n):
            count += 1
            #print 'node: ' + n + ', in_degree: ' + str(G.in_degree(n))
    print 'num of nodes with out degree equal to zero: ' + str(count)        
    return