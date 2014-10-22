#!/usr/local/anaconda/bin/python2.7
'''
Created on Nov 14, 2013

@author: michal

TBD- ADD THE FOLLOWING ATTRIBUTES FOR EACH NODE FOR POSSIBLE CLASSIFICATION AFTERWARDS:

    Number of unique visitors
    Days of week and rush hours
    Domains/countries of host's visitors.
    Hosts list
    total Number of pages views
    Most viewed, entry and exit pages
    File types
    OS used
    Browsers used
    Robots
    HTTP referrer
    HTTP errors
    
'''
from __future__ import division  # this is for FLOAT division (a=b/c , a is float even if b & c are int)
import os
import networkx as nx   #used for graphs
import matplotlib.pyplot as plt #used for graph plots
import trxFunctionsClass
#import functionsClass 
import myPageRank as myPR
from sklearn import cross_validation
import numpy as np
import generalMethods as gm

global Label; Label = trxFunctionsClass.Label
#global dLabel; dLabel = FunctionsClass.dLabel
global keyRiskWeight; keyRiskWeight = trxFunctionsClass.keyRiskWeight

global epsilon; epsilon = 1.0e-6 #0.0001

'''
NumOfVisits = 0
NumOfDistinctVisitors = 1
NumOfRiskyVisitors = 2
NumOfMalwareVisitors = 3
NumOfCopyrightVisitors = 4 
NumOfKeywordVisitors = 5

TotalTimeSpent = 6
AvgTimeSpent = 7
MaxTimeSpent = 8 
InDegree = 9              # In site POV, otherwise it's the same as NumOfDistinctVisitors    TBD
OutDegree = 10            # In site POV, The num of distinct sites the domain contain links for    TBD
UsersInRiskDegree = 11    # NumOfRiskyVisitors / NumOfDistinctVisitors
UsersOutRiskDegree = 12   # If one of the trx in lines with this domain has hasChild=1, find the child and copy its UsersInRiskDegree    TBD
IsInBlackList = 13
TotalNumOfRedirections = 14   # Total num of times the domain redirected to other URLs
NumOfDistinctUrlRedirections = 15  # Num of distinct URLs the site redirected to
NumOfDistinctDomainRedirections = 16   # Num of distinct Domains the site redirected to
'''
# the below 2 classes should be updated when updating addNode and addEdge:
class nLabel(object):   # Node label
    NodeRiskRank = 'NodeRiskRank'                               # isInBlackList (or 0- non, 1-key, 2-copy, 3-mal)
    Popularity = 'Popularity'                                   # Num of visits- Based on edges attributes
    GoodPopularity = 'GoodPopularity'                           # Num of 'good' users visits - Based on edges attributes
    BadPopularity = 'BadPopularity'                             # Num of 'bad' users visits - Based on edges attributes
    TotalTimeSpent = 'TotalTimeSpent'
    AvgTimeSpent = 'AvgTimeSpent'
    MaxTimeSpent = 'MaxTimeSpent'
    GoodScore = 'GoodScore'                                     # Populated by the PageRank algorithm
    BadScore = 'BadScore'                                       # Populated by the PageRank algorithm
    GoodPopPct = 'GoodPopPct'                                   # GoodPopularity / Popularity
    BadPopPct = 'BadPopPct'                                     # BadPopularity / Popularity
    
class eLabel(object):   # Edge label
    Popularity = 'Popularity'                                   # Num of trx
    GoodPopularity = 'GoodPopularity'                           # Num of 'good' users visits
    BadPopularity = 'BadPopularity'                             # Num of 'bad' users visits
    IsLink = 'IsLink'                                           # lines.isLink= 1 
    IsRedirection = 'IsRedirection'                             # lines.httpCode starts with 3XX 
    GoodWeight = 'GoodWeight'                                   # Calculated good weight of the edge- should consider all attributes but BadPopularity, OR could be the ratio between good and bad!!! (Sg/Sb)
    BadWeight = 'BadWeight'                                     # Calculated good weight of the edge- should consider all attributes but GoodPopularity
    GoodPopPct = 'GoodPopPct'                                   # GoodPopularity / Popularity
    BadPopPct = 'BadPopPct'                                     # BadPopularity / Popularity
    
class graph(object):
    dGraph = nx.DiGraph()
    
    def writeGraphToFile(self,filePath):
        graph_as_dict=nx.to_dict_of_dicts(self.dGraph)
        print graph_as_dict
        gm.saveDict(filePath, graph_as_dict)
        return
    
    def addNode(self, nodeName, riskLevel):
        self.dGraph.add_node(nodeName, 
                              NodeRiskRank = riskLevel,                     # isInBlackList (or 0- non, 1-key, 2-copy, 3-mal)
                              Popularity = 0,                               # Num of visits- Based on edges attributes
                              GoodPopularity = 0,                           # Num of 'good' users visits - Based on edges attributes
                              BadPopularity = 0,                            # Num of 'bad' users visits - Based on edges attributes
                              TotalTimeSpent = 0,
                              AvgTimeSpent = 0,
                              MaxTimeSpent = 0,
                              #GoodScore = 0,
                              #BadScore = 0,
                              GoodPopPct = 0,                                   # GoodPopularity / Popularity
                              BadPopPct = 0)                                     # BadPopularity / Popularity
    
        return
    
    def addEdge(self, father, son):
        self.dGraph.add_edge(father, son,
                              Popularity = 0,                               # Num of trx
                              GoodPopularity = 0,                           # Num of 'good' users visits
                              BadPopularity = 0,                            # Num of 'bad' users visits
                              IsLink = 0,                                   # lines.isLink= 1 
                              IsRedirection = 0,                            # lines.httpCode starts with 3XX 
                              #GoodWeight = 0,                               # Calculated good weight of the edge- should consider all attributes but BadPopularity, OR could be the ratio between good and bad!!! (Sg/Sb)
                              #BadWeight = 0,                                # Calculated good weight of the edge- should consider all attributes but GoodPopularity
                              GoodPopPct = 0,
                              BadPopPct = 0)
        return
    
    def addIfNewElement(self, type, arg1, arg2=-1):     # If the method creates a new node/edge- returns 1, else returns 0
        if (arg1 != None):
            if type == 'edge':  # arg1 = father, arg2 = son
                if (arg2 != None):
                    if(not graph.dGraph.has_edge(arg1, arg2)):  # If this edge do not appear in the graph
                            self.addEdge(arg1, arg2)
                            return 1
            elif type == 'node':  # arg1 = domain , arg2 = isRisky (optional)
                if (not graph.dGraph.has_node(arg1)):         # If the domain do not appear in the graph  
                    if (arg2 == -1):    # We shall check first if the domain is risky:
                        riskArray = trxFunctionsClass.isRiskyDomain(arg1)
                        arg2 = trxFunctionsClass.getRiskLevel(riskArray[0], riskArray[1], riskArray[2], riskArray[3])                 
                    self.addNode(arg1, arg2) 
                    return 1                        
        
        return 0
    
    def increaseElementAttrVal(self, type, attr, value, key1, key2=0):
        if type == 'node':  #key2 is not needed here
            self.dGraph.node[key1][attr] += value
        if type == 'edge':
            self.dGraph.edge[key1][key2][attr] += value
        return
    
    def updateElementAttrMaxVal(self, type, attr, value, key1, key2=0):
        if type == 'node':  #key2 is not needed here
            if (self.dGraph.node[key1][attr] < value): self.dGraph.node[key1][attr] = value
        if type == 'edge':
            if (self.dGraph.edge[key1][key2][attr] < value): self.dGraph.edge[key1][key2][attr] = value
        return
    
    def updateElementAttrAvgVal(self, type, attr, numerator, denominator, key1, key2=0):
        if (numerator != 0 and denominator != 0):  
            if type == 'node':  #key2 is not needed here
                self.dGraph.node[key1][attr] = numerator/denominator #+ epsilon
            if type == 'edge':
                self.dGraph.edge[key1][key2][attr] = numerator/denominator #+ epsilon
        else: 
            if type == 'edge':
                self.dGraph.edge[key1][key2][attr] = epsilon
                #print "DomainsGraphClass.updateElementAttrAvgVal:    CANNOT DIVIDE BY ZERO HENCE PUT EPSILON!!!"
        return
    
    def updateNodeAttrWhenNoPrevExist(self, nodeName, userRiskRank):  # updates the node popularity attributes in cases of a node with no prevSite or a new prevSite
        self.increaseElementAttrVal('node', nLabel.Popularity, 1, nodeName)
        if (userRiskRank): self.increaseElementAttrVal('node', nLabel.BadPopularity, 1, nodeName)    # The GoodPopularity will be update in the end by updateGraphAggData (Popularity-BadPopularity)
        return
    
    def handleLine(self,line, userRisk):
        domain = line[Label.domain]
        prevSite = line[Label.prevSite]
        isLink = int(line[Label.isLink])
        httpCode = line[Label.httpCode]                 # For redirections   
        redirectToUrl = line[Label.httpRedirectToUrl]
        timeSpent = float(line[Label.timeSpent]) 
        isRisky = line[Label.isRisky]                   # If line.isRisky = 1, means the Requested Site is risky!!
        isMal = line[Label.malRisk]
        isCopy = line[Label.copyrightRisk]
        isKey = line[Label.keywordRisk]
        
        riskLevel = trxFunctionsClass.getRiskLevel(isRisky, isMal, isCopy, isKey)
        if riskLevel == keyRiskWeight: #KEYWORD found in the URL
            if( trxFunctionsClass.containKeyword(domain) == 0 ):    #Check if the keyword exist in the DOMAIN! (for eliminating cases of google search etc.)
                # The keyword is NOT included in the domain, hence we call getRiskLevel with isKey=zero:
                riskLevel = trxFunctionsClass.getRiskLevel(isRisky, isMal, isCopy, 0)   
        
        # DEBUG: print "userRisk = "+str(userRisk)+"\nreqSite = "+line[Label.reqSite]+"\ndomain = "+domain+"\nprevSite = "+prevSite+"\nisLink = "+str(isLink)+"\nhttpCode = "+httpCode+"\nredirectToUrl = "+redirectToUrl+"\ntimeSpent = "+str(timeSpent)+"\nisRisky = "+str(isRisky)+"\nisMal = "+str(isMal)+"\nisCopy = "+str(isCopy)+"\nisKey = "+str(line[Label.keywordRisk])+"\nriskLevel = "+str(riskLevel)
        #CHECK IF THE DOMAIN IS A USER CONTENT GENERATOR- IF SO, WE SHALL INSERT THE URL AS NODE INSTEAD OF ITS DOMAIN!!!!!!!!!!
        self.addIfNewElement('node', domain, riskLevel)   # Add new edge if not exist
        
        # Update node attributes:
        self.increaseElementAttrVal('node', nLabel.TotalTimeSpent, timeSpent, domain)
        self.updateElementAttrMaxVal('node', nLabel.MaxTimeSpent, timeSpent, domain)
        self.updateElementAttrMaxVal('node', nLabel.NodeRiskRank, riskLevel, domain) # We would like to update the domain risk rank in cases where the initial rank was 0 but we find out later that one of its URLs contains one of the special keywords
        
        # Handle Redirections:
        if (httpCode.startswith('3')): 
            redirectToDomain = trxFunctionsClass.getDomainFromRequestedSite(redirectToUrl)
            if (redirectToDomain != ''):
                self.addIfNewElement('node', redirectToDomain)  # Add new node if not exist
                self.addIfNewElement('edge', domain, redirectToDomain)  # Add new edge if not exist
                self.updateElementAttrMaxVal('edge', eLabel.IsRedirection, 1, domain, redirectToDomain)   
            # DEBUG: printElementAttr(domain, redirectToDomain) 
            
        if (prevSite != None):    # There is a prevSite in the trx
            prevDomain = trxFunctionsClass.getDomainFromRequestedSite(prevSite)
            if (prevDomain != ''):
                self.addIfNewElement('node', prevDomain)
                self.addIfNewElement('edge', prevDomain, domain)   # Add new edge if not exist
                # Update edge attributes:
                self.increaseElementAttrVal('edge', eLabel.Popularity, 1, prevDomain, domain)
                if (userRisk != 0): self.increaseElementAttrVal('edge', nLabel.BadPopularity, 1, prevDomain, domain) # The GoodPopularity will be updated in the end by Popularity-BadPopularity (in updateGraphAggData)
                if (isLink == 1): self.updateElementAttrMaxVal('edge', eLabel.IsLink, 1, prevDomain, domain)
                
                ''' the reason for the below comment explained in the 'else' part comment at the end of this method
                if ( addIfNewElement('node', prevDomain, prevSite) ): # If this is a new node- add it and then increase its popularity attributes:
                    updateNodeAttrWhenNoPrevExist(prevDomain, userRisk)
                '''
                
            # DEBUG: printElementAttr(prevDomain, domain)
            
        #print "out degree: " + str(dGraphObj.out_degree(domain))
    
        ''' I am interested in the edges weight only- the first step is not relevant- only the path itself, as per PageRank POV
        else:   # There is NO prevSite in the trx
            updateNodeAttrWhenNoPrevExist(domain, userRisk)
        '''
                   
        # DEBUG: printElementAttr(domain)     
             
        return
    
    def updateGraphAggData(self):
        for (u,v,d) in graph.dGraph.edges(data=True):       # u=from node, v=to node, d=dictionary of the edge attributes
            pop = d[eLabel.Popularity]
            badPop = d[eLabel.BadPopularity]
            goodPop =  pop - badPop                 # GoodPopularity=Popularity-BadPopularity
            self.increaseElementAttrVal('edge', eLabel.GoodPopularity, goodPop, u, v)
            self.updateElementAttrAvgVal('edge', eLabel.GoodPopPct, goodPop, pop, u, v)
            self.updateElementAttrAvgVal('edge', eLabel.BadPopPct, badPop, pop, u, v)
            
        ''' PageRank counts on theedges weight only... IT IS RELEVANT FOR FUTURE ANALYSIS VIA SUPERVISED LEARNING!!!    
        for (n,a) in graph.dGraph.nodes(data=True):         # n=node, d=dictionary of the node attributes
            increaseElementAttrVal('node', nLabel.GoodPopularity, a[nLabel.Popularity] - a[nLabel.BadPopularity], n) # first update the node GoodPopularity with the data related to cases when no preSite exists: GoodPopularity=Popularity-BadPopularity
            increaseElementAttrVal('node', nLabel.Popularity, graph.dGraph.in_degree(n, weight=nLabel.Popularity), n) # then update the node Popularities with the edges attributes
            increaseElementAttrVal('node', nLabel.GoodPopularity, graph.dGraph.in_degree(n, weight=nLabel.GoodPopularity), n)     
            increaseElementAttrVal('node', nLabel.BadPopularity, graph.dGraph.in_degree(n, weight=nLabel.BadPopularity), n)
            updateElementAttrAvgVal('node', nLabel.BadPopPct, a[nLabel.BadPopularity], a[nLabel.Popularity], n)
            updateElementAttrAvgVal('node', nLabel.GoodPopPct, a[nLabel.GoodPopularity], a[nLabel.Popularity], n)
            updateElementAttrAvgVal('node', nLabel.AvgTimeSpent, a[nLabel.TotalTimeSpent], a[nLabel.Popularity], n)
        '''
            
        
        return    
            
    def updateGraphFromDomainsContainer(self, domains):   #TBD
        #update nodeRiskRank (isInBlackList), InNumOfRiskyUsers, InTotalNumOfUsers, AvgTimeSpent, MaxTimeSpent, NumOfDistinctUrlRedirections, NumOfDistinctDomainRedirections
        return
    
    def graphPlot(self, path):
        #plt.savefig("/home/michal/Desktop/path.png")
        nx.draw(self.dGraph)
        plt.savefig(path)
        return
    
    def printGraphAttr(self, type):
        if type == 'node':
            for nodeName in self.dGraph.nodes():
                print nodeName + " :    " + str(self.dGraph.node[nodeName]) + "\n"
                
        if type == 'edge':
            for edgeName in self.dGraph.edges():
                print str(edgeName) + " :    " + str(self.dGraph.edge[edgeName[0]][edgeName[1]]) + "\n"
                
        print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        return
    
    def printElementAttr(self, key1,key2=0): 
        if key2:    #  This is an edge
            print key1 + " , " + key2 + " :    " + str(self.dGraph.edge[key1][key2])
        else:       # This is a node
            print key1 +  " :    " + str(self.dGraph.node[key1])
        return
        
        



def runPageRank(tarPath):
    # GINNA: tarPath = '/home/michal/Desktop/debugFile_PageRank'
    os.path.exists(tarPath) and os.remove(tarPath)
    debugFile = open(tarPath, 'a')
    # Create the personalization vector- in the original PageRank this is the popularity distribution of the pages. its default is uniform dist. 
    # Means, that in (1-alpha) = 0.15 the user will get bored and will type a different address in the URL box, where the probability of jumping to diff page is its personalization value 
    # In our case this personalization will represent the seed of malicious sites. 
    # Intuitive explanation- we give a different weight for each 'jumping' event to a different site as per its risk level. 
    # Check few personalization: 1/N-if the site is risky, 0-otherwise. N=num of risky sites (for normalizing- the sum of personalization vector should be 1)
    #                            the node risk rank (0,1,2,3) / N, where N is the sum of all nodes risk ranks
    #                            Pr(X=specificMalSite|X=malSite)    this is the malicious popularity (the site popularity upon the mal sites)
    #personalization = graph.dGraph.nodes(weight=nLabel.NodeRiskRank)
    initRiskRank = dict ({})
    for (n,d) in graph.dGraph.nodes(data=True):  
        if (d[nLabel.NodeRiskRank]): initRiskRank[n] = d[nLabel.NodeRiskRank]
        else: initRiskRank[n] = epsilon
        #DEBUG:
        if (d[nLabel.NodeRiskRank] >= 1): debugFile.write("\nnode: " + n + " ,    rank: " + str(d[nLabel.NodeRiskRank]))
    
    #DEBUG:
    degree = graph.dGraph.out_degree(weight=nLabel.BadPopPct)
    for (u,v,d) in graph.dGraph.edges(data=True):
        if degree[u]==0: 
            debugFile.write("\n\nZERO DEGREE:    u = " + u + " , v = " + v + " , degree = " + str(degree[u]) + " , in_degree = " + str(graph.dGraph.in_degree(u,weight=nLabel.BadPopPct))+ " , out_degree = "+ str(graph.dGraph.out_degree(u,weight=nLabel.BadPopPct)))
            debugFile.write("\n  NEIGHBORS:    "+str(graph.dGraph.neighbors(u)))
            debugFile.write("\n  DATA:")
            for i in d:
                debugFile.write( "\n    "+i + " :    " + str(d[i]))
    print "IS ABOUT TO CALL PageRank!!!!!!!!!!!!!!!!"    
    #initRiskRank = graph.dGraph.nodes(weight=nLabel.NodeRiskRank) # In pagerank_alg there is a normalization on nstart anyway 
    
    # Bad Popularity propagation:
    #BadPR = myPR.pagerank(graph.dGraph,personalization=initRiskRank,nstart=initRiskRank,weight=eLabel.BadPopPct)
    BadPR = myPR.pagerank(graph.dGraph,weight=eLabel.BadPopPct)

    
    debugFile.write( "\n\n\n\nNum of nodes in the graph: " + str(nx.number_of_nodes(graph.dGraph)) )
    # Print a list of tuples (domain, PageRank) ordered by DESC values:
    debugFile.write( "\n\nBadPR - personalization, nstart - DESC SORTED!! #####\n" + str(sorted(BadPR.items(), key=lambda x: (-x[1], x[0]))) ) 
    #PageRank counts edges only!!    debugFile.write( "\n\nNodes BadPopPct #####\n" + str(sorted(nx.get_node_attributes(graph.dGraph,nLabel.BadPopPct).items(), key=lambda x: (-x[1], x[0]))))
    debugFile.write( "\n\nIn Degree of BadPopPct #####\n" + str(sorted(graph.dGraph.in_degree(weight=eLabel.BadPopPct).items(), key=lambda x: (-x[1], x[0]))))
    debugFile.write( "\n\nInitial Nodes Risk Rank #####\n" + str(sorted(nx.get_node_attributes(graph.dGraph,nLabel.NodeRiskRank).items(), key=lambda x: (x[1], x[0]))))
      
    trxFunctionsClass.writeHashWithValuesToFile(BadPR, '/home/michal/Desktop/PageRankOutput')
    

    #PRaccuracy = leaveOneOutEvaluation('ME', initRiskRank, BadPR)
    PRaccuracy = StratifiedKFold('ME', initRiskRank, 10)
    print "ME:    "+str(PRaccuracy)
    

    '''
    BadPR = nx.pagerank(graph.dGraph,personalization=initRiskRank,weight=eLabel.BadPopPct)
    debugFile.write("\n\nBadPR - personalization\n" + str(BadPR))
    BadPR = nx.pagerank(graph.dGraph,nstart=initRiskRank,weight=eLabel.BadPopPct)
    debugFile.write("\n\nBadPR - nstart\n" + str(BadPR))
    BadPR = nx.pagerank(graph.dGraph,weight=eLabel.BadPopPct)
    debugFile.write("\n\nBadPR - \n" + str(BadPR))
    '''
    # Good Popularity propagation:
    #GoodPR = nx.pagerank(graph.dGraph,weight=eLabel.GoodPopPct)
    #print "\nBadPR: " + str(BadPR); print "\nGoodPR: " + str(GoodPR)
    
    return

def leaveOneOutEvaluation(accuracyMeasure, initRiskRank, PRDict):
    accuracy = 0
    errors = []
    initRiskRankSeed = dict((k,v) for k, v in initRiskRank.items() if v > 1)   #create a dict of the seed (domain,RiskRank)- for mal and key only!
    normFactor = sum(initRiskRank.values())
    
    names = ['domain','riskRank']
    formats = ['|S100','f8']
    dtype = dict(names = names, formats = formats)
    initRiskRankSeed_npArray = np.array(initRiskRankSeed.items(), dtype=dtype)
    
    loo = cross_validation.LeaveOneOut(len(initRiskRankSeed_npArray))
    print(loo)

    for train_index, test_index in loo:
        initRiskRank_tmp = initRiskRank.copy()

        testKey = initRiskRankSeed_npArray[test_index][0][0]
        testVal = initRiskRankSeed_npArray[test_index][0][1]
        initRiskRank_tmp[testKey] = epsilon
        
        iPR = myPR.pagerank(graph.dGraph, personalization=initRiskRank_tmp, nstart=initRiskRank_tmp, weight=eLabel.BadPopPct, tol=1.0e-10, max_iter=200)[testKey]
        errors += [ abs((testVal/normFactor) - iPR) ]
        initRiskRank_tmp.clear()
        
        
        '''
        print " "
        print("TRAIN:", train_index, "TEST:", test_index)
        initRiskRankSeed_train = np.array(initRiskRankSeed_npArray[train_index], dtype=dtype)
        initRiskRankSeed_test = np.array(initRiskRankSeed_npArray[test_index], dtype=dtype)
        #initRiskRankSeed_train = np.array(initRiskRankSeedTuples[train_index][1])
        #initRiskRankSeed_test = np.array(initRiskRankSeedTuples[test_index][1])
        print "TRAIN :" + str(initRiskRankSeed_train)
        print "TEST :"+str( initRiskRankSeed_test)
        '''
        
          
    ''''FOR TESTING ONLY:
    nstartTest = initRiskRank.copy()
    for t in nstartTest.keys():
        nstartTest[t] = abs(nstartTest[t]-3)
        if nstartTest[t] <= 2:
            nstartTest[t] = epsilon
    '''
    '''
    for i in initRiskRankSeed.keys():
        iPR = 0
        initRiskRankTmp = initRiskRank.copy()   #shallow copy- creates new references for initRiskRankws content
        initRiskRankTmp[i] = epsilon    #take domain i out of the seed
        #iPR = myPR.pagerank(graph.dGraph, personalization=initRiskRankTmp, nstart=initRiskRankTmp, weight=eLabel.BadPopPct)[i]
        #iPR = myPR.pagerank(graph.dGraph, personalization=PRDict, weight=eLabel.BadPopPct)[i]
        iPR = myPR.pagerank(graph.dGraph, weight=eLabel.BadPopPct)[i]
        errors += [ abs((initRiskRankSeed[i]/normFactor) - iPR) ]
        #update and clear the temp params:
        initRiskRankTmp.clear()
    '''
    
        
    
    if accuracyMeasure == 'ME':
        accuracy = sum(errors)/len(errors)
        
    return accuracy

def StratifiedKFold(accuracyMeasure, initRiskRank, K):
    
    
    accuracy = 0
    errors = []
    initRiskRankSeed = dict((k,v) for k, v in initRiskRank.items() if v >= 1)   #create a dict of the seed (domain,RiskRank)- for mal and key only!
    normFactor = sum(initRiskRank.values())
    
    #DEBUG:
    print "len of seed = " + str(len(initRiskRankSeed)) + " out of : " +str(len(initRiskRank)) + " nodes"
    
    names = ['domain','riskRank']
    formats = ['|S100','f8']
    dtype = dict(names = names, formats = formats)
    initRiskRankSeed_npArray = np.array(initRiskRankSeed.items(), dtype=dtype)
    riskRankLabels = np.array(initRiskRankSeed.values())
    
    skf = cross_validation.StratifiedKFold(riskRankLabels, n_folds=K)
    #DEBUG: print(skf)
    for train_index, test_index in skf:
        initRiskRank_tmp = initRiskRank.copy()
        testKeys = []
        for i in test_index:
            testKeys.append(initRiskRankSeed_npArray[i][0])
            initRiskRank_tmp[testKeys[-1]] = epsilon    #testKeys[-1] = last element in testKeys list
        
        iPR = myPR.pagerank(graph.dGraph, personalization=initRiskRank_tmp, nstart=initRiskRank_tmp, weight=eLabel.BadPopPct, tol=1.0e-10, max_iter=200)
        #iPR = myPR.pagerank(graph.dGraph, tol=1.0e-10, max_iter=200)
        foldErrors = []
        for k in testKeys:
            foldErrors += [ abs((initRiskRankSeed[k]/normFactor) - iPR[k]) ]
        errors.append(sum(foldErrors)/len(foldErrors))
        #clean containers:
        del foldErrors[:]   
        del testKeys[:]
        del test_index
        initRiskRank_tmp.clear()
        iPR.clear()
        
    if accuracyMeasure == 'ME':
        accuracy = sum(errors)/len(errors)
        
    return accuracy

    

#-------------------------------------------------------------------------------------------------------
# DEBUG METHODS:


G=graph()   #Instantiation
