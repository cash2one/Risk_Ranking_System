#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 21, 2014

@author: michal
'''
import generalMethods as gm
import linesClass 

global eps; eps = 0.0001    # epsilon (for CN edges of self links)

class TransitionsDict():
    TD = dict()         # 'Transition matrix' as dict 
    DRD = dict()        # Domain Risk Rank Dict - will be used as the seed (nstart) for SALSA
    
    def updateEdge(self,fn,sn,is_link=1):  
        # fn = father node (name)
        # sn = son node (name)
        # is_link = (int 0 or 1) when you want to create a graph with relation to hyper-links 
        #    you send here the http 'is_link' param. 
        #    when relation to hyper-links is not relevant use the default value 1 for all edges.
        if fn and sn:   #if they are not empty!!
            self.TD.setdefault(fn,{}).setdefault(sn, {'weight': 0, 'is_link': 0})    # Set default values if edge don't exist
            self.TD[fn][sn]['is_link'] = max(is_link,self.TD[fn][sn]['is_link'])
        return
    
    def calcEdgeWeight(self,fn,sn,link_weight=1.):
        # fn = father node (name)
        # sn = son node (name)
        # link_weight = (float [0,1]) represents the gap between hyper-link edge weight to non hyper-link edge weight.
        #    for example- edge details: 'is_link'=1, link_weight=0.7 => weight=1
        #                 edge details: 'is_link'=0, link_weight=0.7 => weight=0.3
        #     when link_weight=1. non hyper-link edges weight will be 0 (a hyper-link graph)
        is_link = self.TD[fn][sn]['is_link']
        self.TD[fn][sn]['weight'] = (1.-link_weight) + is_link*link_weight
        return
    
    def calcWeights(self,link_weight=1.):
        for k in self.TD.keys():
            for nested_k in self.TD[k].keys():
                self.calcEdgeWeight(k, nested_k,link_weight=link_weight)
        return
    
          
    def extractArgsFromLine(self,line,argsList):
        results = []
        for arg in argsList:
            results.append(line[arg]) 
            
        if len(results) == 1:   return results[0]   # don't return it as a list!
        else:                   return results
    
    def handleLine(self,line,prevDomain,curDomain,link_ref=False):
        # line (preprocessed array from the log) is needed here just for extracting the user id for now
        if link_ref: # increases the edge's weight if it represents a link (and bad users passed on it) 
            isLink = self.extractArgsFromLine(line, [l.isLink])
            self.updateEdge(prevDomain, curDomain,is_link=int(isLink))
        else:
            self.updateEdge(prevDomain, curDomain)
        
        # Update Domain Risk Rank Dict: 
        self.updateDomainRiskDict(line, curDomain, prevDomain)
        '''self.updateDomainRiskDict(curDomain, line) 
        if prevDomain and prevDomain != curDomain:     # if it is not a self link
            self.updateDomainRiskDict(prevDomain)'''       
        return
    
    def updateDomainRiskDict(self,line,curDomain,prevDomain=None):
        if curDomain not in self.DRD:
            self.DRD[curDomain] = line[l.riskRank]
        if prevDomain and prevDomain != curDomain:
            if prevDomain not in self.DRD:
                self.DRD[prevDomain] = line[l.prevDomainRiskRank]
        return 
    
    def remove_zero_weight_edges(self):
        d = {}
        for fn in self.TD:
            for sn in self.TD[fn]:
                if self.TD[fn][sn]['weight'] == 0 : d.setdefault(fn,[]).append(sn)
        for fn in d:
            for sn in d[fn]:
                del self.TD[fn][sn]
                self.TD.setdefault(sn,{}) # for cases where the son node we just deleted not existing as father node- 
                #                            if we won't do this the risk is that the son node won't appear at all in the graph!
        return
    
    def buildTransitionDict(self,lines,link_ref=False,link_weight=1.):            
        # lines is the preprocessed log as list
        # we still care about (broeser) sessions- cause that's separating between the users - DO WE?????
        
        # init the prevSession to be the first line session, so it won't pass the first line domain
        # cause now for the first line the following is true- curSession = prevSession 
        #prevSession = self.extractArgsFromLine(lines[0], [l.bSesId])
        for line in lines[0:len(lines)]:          
            (prevDomain, curDomain) = self.extractArgsFromLine(line, [l.prevDomain, l.domain])
            self.handleLine(line, prevDomain, curDomain, link_ref=link_ref)
        self.calcWeights(link_weight=link_weight)
        if link_ref:    # if there is a relation to actual hyper-link edges, remove the edges with weight zero (possible if link_weight is 1)
            self.remove_zero_weight_edges()       
        return
    
    def writeTransDictToFile(self,fileName):
        gm.saveDict(fileName, self.TD)
        return
    
    def writeDomainRiskDictToFile(self,fileName):
        gm.saveDict(fileName, self.DRD)
        return
    
    def clear(self):
        self.TD.clear()
        self.DRD.clear()
        return
    
    
TransitionsDictObj = TransitionsDict()   #instantiation
l = linesClass.Label()   # lines labels instantiation    
        
