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
    CN = 'CN'           # CN = Central Node (connected to every first and last domain of each session)
    DRD = dict()        # Domain Risk Rank Dict - will be used as the seed (nstart) for SALSA
    
    def updateEdge(self,fn,sn,user_risk=0):  
        # If a bad user moved from fn to sn- use: updateEdge(fn,sn, user_risk=1) 
        # If a good user moved from fn to sn- use: updateEdge(fn,sn) 
        if fn and sn:   #if they are not empty!!
            self.TD.setdefault(fn,{}).setdefault(sn, {'g':0, 'b':0, 'weight': 0})    # Set default values if edge don't exist
            if not user_risk:           # If g not zero (means good user)
                self.TD[fn][sn]['g'] += 1
            else:               # g=0 (means bad user)
                self.TD[fn][sn]['b'] += 1 
        return
    
    def updateArtificialEdge(self,fn,sn):   # for edges related to CN or self link
        if fn and sn:   #if they are not empty!!
            self.TD.setdefault(fn,{}).setdefault(sn, {'weight': eps})
        return
     
    def openSession(self,n):
        if n:   # if n not empty
            self.updateArtificialEdge(self.CN, n)
        return
    
    def closeSession(self,n):
        if n:   # if n not empty
            self.updateArtificialEdge(n, self.CN)
        return
       
    def calcEdgeWeight(self,fn,sn):
        if not self.TD[fn][sn]['weight']:   # The edge's weight=0 (if not it means it's related to CN-with eps weight)
            pure_good_weight = eps*10
            b = float(self.TD[fn][sn]['b'])
            g = float(self.TD[fn][sn]['g'])
            if not b:                       # The edge's 'b'=0 (only good users passed here)
                self.TD[fn][sn]['weight'] = pure_good_weight#eps
            else:                           # The edge's 'b'>0 
                if g:                       # The edge's 'g'>0 (good and bad users passed)
                    self.TD[fn][sn]['weight'] = b/(b+g)
                else:                       # The edge's 'g'=0 (only bad users passed here)
                    self.TD[fn][sn]['weight'] = 1
        return
    
    def calcWeights(self):
        for k in self.TD.keys():
            for nested_k in self.TD[k].keys():
                self.calcEdgeWeight(k, nested_k)
        return
    
    def addSelfLinks(self):
        for k in self.TD.keys():
            self.updateArtificialEdge(k, k)
        return
    
    def extractArgsFromLine(self,line,argsList):
        '''curSession = line[l.genSesId]
        prevDomain = line[l.prevSite]
        curDomain = line[l.domain]'''
        results = []
        for arg in argsList:
            results.append(line[arg]) 
            
        if len(results) == 1:   return results[0]   # don't return it as a list!
        else:                   return results
    
    def handleFirstLine(self,line):
        # prevDomain in line not relevant here at all
        #(curSession, curDomain) = self.extractArgsFromLine(line, [l.genSesId, l.domain])
        (curSession, curDomain) = self.extractArgsFromLine(line, [l.bSesId, l.domain])
        self.openSession(curDomain)
        self.updateDomainRiskDict(curDomain, line)  
        return curSession, curDomain
    
    def handleLastLine(self,line):
        curDomain = self.extractArgsFromLine(line, [l.domain])
        self.closeSession(curDomain) 
        
        # Update Domain Risk Rank Dict: 
        self.updateDomainRiskDict(curDomain, line) 
        prevDomain = self.extractArgsFromLine(line, [l.prevDomain])    #self.extractArgsFromLine(line, [l.prevSite])
        if prevDomain and prevDomain!=curDomain:
            self.updateDomainRiskDict(prevDomain)
        return
    
    def handleLine(self,line,prevDomain,curDomain,uRisk):
        # line (preprocessed array from the log) is needed here just for extracting the user id for now
        # uRisk is users risk rank dict
        self.updateEdge(prevDomain, curDomain, user_risk=uRisk[line[l.uId]])
        
        # Update Domain Risk Rank Dict: 
        self.updateDomainRiskDict(curDomain, line) 
        if prevDomain and prevDomain != curDomain:     # if it is not a self link
            self.updateDomainRiskDict(prevDomain)
        
        return
    
    def updateDomainRiskDict(self,n,line=None):
        # n is a domain (node)
        #line is for extracting its risk score
        if n not in self.DRD:
            if line:        # if the node is the the current domain in 'line'
                self.DRD[n] = self.extractArgsFromLine(line, [l.riskRank])       #TBD- change isRisky to riskScore!!!! (in 'lines' building)          
            else:           # line = None
                self.DRD[n] = 0
        else:               # node exists in Domain Risk Rank Dict- we shall update its value as per the max of them
            if line:        
                self.DRD[n] = max(self.DRD[n], self.extractArgsFromLine(line, [l.riskRank]))
        return 
    
    def buildTransitionDict(self,lines,uRisk):            
        # lines is the preprocessed log as list
        # uRisk is the users risk rank dictt
        (prevSession, last_domain_in_session) = self.handleFirstLine(lines[0])
        curDomain = ''
        
        for line in lines[1:len(lines)-2]:          # 'lines' without the first and last lines 
            #(curSession, prevDomain, curDomain) = self.extractArgsFromLine(line, [l.genSesId, l.prevDomain, l.domain])
            (curSession, prevDomain, curDomain) = self.extractArgsFromLine(line, [l.bSesId, l.prevDomain, l.domain])
            if curSession == prevSession:           # same session
                self.handleLine(line, prevDomain, curDomain, uRisk)
            else:                                   # new session
                self.closeSession(last_domain_in_session)
                self.openSession(curDomain)
            last_domain_in_session = curDomain
            prevSession = curSession
        
        self.handleLastLine(lines[len(lines)-1])
        
        self.calcWeights()
        #self.addSelfLinks()
        
        return
    
    def writeTransDictToFile(self,fileName):
        gm.saveDict(fileName, self.TD)
        return
    
    def writeDomainRiskDictToFile(self,fileName):
        gm.saveDict(fileName, self.DRD)
        return
    
    def clear(self):
        self.DRD.clear()
        self.TD.clear()
        return
    
    
TransitionsDictObj = TransitionsDict()   #instantiation
l = linesClass.Label()   # lines labels instantiation    
        
