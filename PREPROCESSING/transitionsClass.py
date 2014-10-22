#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 21, 2014

@author: michal
'''
import generalMethods as gm
import linesClass 

global eps; eps = 0.0001    # epsilon (for CN edges of self links)

class edge_attributes():
    g = 'g'
    b = 'b'
    w = 'weight'
    is_l = 'is_link'
    is_r = 'is_redirect'
    
class TransitionsDict():
    TD = dict()         # 'Transition matrix' as dict 
    DRD = dict()        # Domain Risk Rank Dict - will be used as the seed (nstart) for SALSA
    e_atr = edge_attributes() #instantiation of edge_attributes for uniformity
    
    def updateEdge(self,fn,sn,user_risk=0,is_link=0,is_redirect=0):  
        # If a bad user moved from fn to sn- use: updateEdge(fn,sn, user_risk=1) 
        # If a good user moved from fn to sn- use: updateEdge(fn,sn) 
        
        # fn = father node (name)
        # sn = son node (name)
        # is_link = (int 0 or 1) when you want to create a graph with relation to hyper-links 
        #    you send here the http 'is_link' param. 
        #    when relation to hyper-links is not relevant use the default value 1 for all edges.
        # is_redirect = (int 0 or 1) create a graph with relation to redirections (when equal to 1)
        
        if fn and sn:   #if they are not empty!!
            self.TD.setdefault(fn,{}).setdefault(sn, {self.e_atr.g:0, self.e_atr.b:0, self.e_atr.w:0, self.e_atr.is_l:0, self.e_atr.is_r:0})    # Set default values if edge don't exist
            
            #self.TD[fn][sn][self.e_atr.is_l] = max(is_link, self.TD[fn][sn][self.e_atr.is_l])
            #self.TD[fn][sn][self.e_atr.is_r] = max(is_redirect, self.TD[fn][sn][self.e_atr.is_r])
            if is_link:         self.TD[fn][sn][self.e_atr.is_l] = 1
            if is_redirect:     self.TD[fn][sn][self.e_atr.is_r] = 1
            
            if not user_risk:           # If g not zero (means good user)
                self.TD[fn][sn][self.e_atr.g] += 1 
            else:                       # g=0 (means bad user)
                self.TD[fn][sn][self.e_atr.b] += 1
        return
          
    def calcEdgeWeight(self,fn,sn,l_w=0.,r_w=0.):
        # fn = father node (name)
        # sn = son node (name)
        # l_w = link weight (float [0,1]) represents the gap between hyper-link edge weight to non hyper-link edge weight.
        #    for example- edge details: 'b'=1, 'g'=0, 'is_link'=1, l_w=0.7 => weight=1
        #                 edge details: 'b'=1, 'g'=0, 'is_link'=0, l_w=0.7 => weight=0.3
        #     when l_w=1. non hyper-link edges weight will be 0 (a hyper-link graph)
        
        if (l_w + r_w > 1): raise NameError('The sum of link and redirection weights should be less than 1!')
        
        pure_good_weight = eps*10
        b = float(self.TD[fn][sn][self.e_atr.b])
        g = float(self.TD[fn][sn][self.e_atr.g])
        is_link = self.TD[fn][sn][self.e_atr.is_l]
        is_redirect = self.TD[fn][sn][self.e_atr.is_r]
        
        if not b:                       # The edge's 'b'=0 (only good users passed here)
            w = pure_good_weight
        else:                           # The edge's 'b'>0 
            if g:                       # The edge's 'g'>0 (good and bad users passed)
                w = b/(b+g)
            else:                       # The edge's 'g'=0 (only bad users passed here)
                w = 1
        self.TD[fn][sn][self.e_atr.w] = w*( (1.-l_w-r_w) + is_link*l_w + is_redirect*r_w)
        return
    
    def calcWeights(self,l_w=0.,r_w=0.):
        for k in self.TD:#.keys():
            for nested_k in self.TD[k]:#.keys():
                self.calcEdgeWeight(k, nested_k,l_w=l_w,r_w=r_w)
        return
    
    def addSelfLinks(self):
        for k in self.TD:#.keys():
            self.updateArtificialEdge(k, k)
        return
    
    def extractArgsFromLine(self,line,argsList):
        results = []
        for arg in argsList:
            results.append(line[arg]) 
            
        if len(results) == 1:   return results[0]   # don't return it as a list!
        else:                   return results
       
    def handleLine(self,line,uRisk,link_ref=False,redirect_ref=False):
        # line (preprocessed array from the log) is needed here just for extracting the user id for now
        # uRisk is users risk rank dict
        prevDomain,curDomain, uId, isLink, redirDomain = self.extractArgsFromLine(line, [l.prevDomain, l.domain, l.uId, l.isLink, l.RedirDomain])
        
        if link_ref: # increases the edge's weight if it represents a link (and bad users passed on it) 
            is_link = int(isLink)
            #self.updateEdge(prevDomain, curDomain, user_risk=uRisk[uId],is_link=int(isLink)) 
        else:   # link_ref=False, The edge's weight influenced only by the users passed on it
            is_link = None
            #self.updateEdge(prevDomain, curDomain, user_risk=uRisk[line[l.uId]])
        self.updateEdge(prevDomain, curDomain, user_risk=uRisk[uId],is_link=is_link)
        
        if redirect_ref and redirDomain:    # If redirection occurred
            self.updateEdge(curDomain, redirDomain, user_risk=uRisk[uId], is_redirect=1)
            
        # Update Domain Risk Rank Dict: 
        self.updateDomainRiskDict(line, redirect_ref)      
        return
    
    def updateDomainRiskDict(self,line,redirect_ref=False):
        #curDomain, prevDomain, redirectDomain = self.extractArgsFromLine(line, [l.domain, l.prevDomain, l.RedirDomain])
        cDomain, cRisk, pDomain, pRisk, rDomain, rRisk\
         = self.extractArgsFromLine(line, [l.domain,l.riskRank, l.prevDomain,l.prevDomainRiskRank, l.RedirDomain,l.RedirDomainRiskRank])
        
        self.DRD.setdefault(cDomain,cRisk)  # requested (current) URL domain
        if pDomain: self.DRD.setdefault(pDomain,pRisk)  # previous URL domain
        if redirect_ref and rDomain:
            self.DRD.setdefault(rDomain,rRisk)  # redirect to URL domain
            
        '''if curDomain not in self.DRD:
            self.DRD[curDomain] = line[l.riskRank]
        if prevDomain and prevDomain != curDomain:
            if prevDomain not in self.DRD:
                self.DRD[prevDomain] = line[l.prevDomainRiskRank]
        if redirect_ref:
            if redirectDomain and redirectDomain != curDomain:
                if redirectDomain not in self.DRD:
                    self.DRD[redirectDomain] = line[l.RedirDomainRiskRank]'''
        return 
    
    def remove_zero_weight_edges(self):
        d = {}
        for fn in self.TD:
            for sn in self.TD[fn]:
                if self.TD[fn][sn][self.e_atr.w] == 0 : d.setdefault(fn,[]).append(sn)
        for fn in d:
            for sn in d[fn]:
                del self.TD[fn][sn]
                self.TD.setdefault(sn,{}) # for cases where the son node we just deleted not existing as father node- 
                #                            if we won't do this the risk is that the son node won't appear at all in the graph!
        return
    
    def buildTransitionDict(self,lines,uRisk,link_ref=False,link_weight=0.,redirect_ref=False,redirect_weight=0.):            
        # lines is the preprocessed log as list
        # uRisk is the users risk rank dictt
        # we still care about (broeser) sessions- cause that's separating between the users - DO WE?????
        
        # init the prevSession to be the first line session, so it won't pass the first line domain
        # cause now for the first line the following is true- curSession = prevSession 
        #prevSession = self.extractArgsFromLine(lines[0], [l.bSesId])
        for line in lines[0:len(lines)]:         
            #(curSession, prevDomain, curDomain) = self.extractArgsFromLine(line, [l.genSesId, l.prevDomain, l.domain])
            #(curSession, prevDomain, curDomain) = self.extractArgsFromLine(line, [l.bSesId, l.prevDomain, l.domain])
            #if curSession == prevSession:           # same session
            self.handleLine(line, uRisk, link_ref=link_ref, redirect_ref=redirect_ref)
            
            #last_domain_in_session = curDomain
            #prevSession = curSession
        
        self.calcWeights(l_w=link_weight,r_w=redirect_weight)
        if (link_ref or redirect_ref):    # if there is a relation to actual hyper-link/redirection edges, remove the edges with weight zero (e.g. possible if link_weight is 1)
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
        
