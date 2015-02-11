#!/usr/local/anaconda/bin/python2.7
'''
Created on Oct 31, 2013

@author: michal
'''


from collections import defaultdict
from operator import itemgetter #used for sorting the file
import os #used for deleting files
#import re #used for regular expressions
import trxFunctionsClass
import linesClass
import domainsGraphClass as dGraphClass
import generalMethods as gm

#global lines; lines = linesClass.Logs.lines;
#global l; l=linesClass.Logs(); global lines; lines = l.lines;
global l; l=linesClass.l; 
global Label; Label=linesClass.lbl  #Label = trxFunctionsClass.Label
#global dGraphClass; dGraphClass = dGraphClass.graph
#global dGraphObj; dGraphObj = dGraphClass.graph.dGraph
global G; G=dGraphClass.G;
global users; global sessions; global domains; global domainsUsers; global domainsRedirections; global usersActDis; global usersIP;


global duLabel; duLabel = dict ({ 'UserId' : 'NumOfVisits'})

global TimeSpentThreshold; TimeSpentThreshold = 6                   #Under this threshold (in sec) we do NOT print to output file
global timeOut; timeOut = 1800                                      # Seconds.  30Min for session segmentation.
        
class uLabel:
    NumOfSessions = 0
    TotalNumOfTrx = 1 
    TotalSessionDuration = 2    
    MaxTimeSpentInSites = 3    
    TotalNumOfCountries = 4    
    AvgSessionDuration = 5    
    AvgTimeSpentInSites = 6 
    AvgTrxInSession = 7   # This is the "Avg Activity Vol" upon sessions
    #AvgCountries = 8       
    TotalNumOfRiskyTrx = 8 # Num of transactions where "isRisky" = 1
    BadActivityVolPct = 9 # Total bad transactions (isRisky=1) divided by TotalNumOfTrx
    isRisky = 10       # Risk Indicator - if malware OR copyright OR keyword
    malRisk = 11        # Indicator, 1 = include malware black list 
    copyrightRisk = 12  # Indicator, 1 = include Google removed domains (copyrights) 
    keywordRisk = 13    # Indicator, 1 = include keywords
    DayInWeek = 14
    IsWeekend = 15
    CountryId = 16     # if more than 1 exist- take the main country)    ???
    NumOfDistinctIPs = 17
    MorningActivityPct = 18
    MorningRiskyActivityPct = 19
    NoonActivityPct = 20
    NoonRiskyActivityPct = 21
    EveningActivityPct = 22
    EveningRiskyActivityPct = 23 
    NightActivityPct = 24
    NightRiskyActivityPct = 25
   
class uDayLabel:
    MorningTotalActivity = 0
    MorningTotalRiskyActivity = 1
    NoonTotalActivity = 2
    NoonTotalRiskyActivity = 3
    EveningTotalActivity = 4
    EveningTotalRiskyActivity = 5 
    NightTotalActivity = 6
    NightTotalRiskyActivity = 7
    SundayTrx = 8
    MondayTrx = 9
    TuesdayTrx = 10
    WednesdayTrx = 11
    ThursdayTrx = 12
    FridayTrx = 13
    SaturdayTrx = 14
 
class sLabel:
    UserId = 0
    NumOfTrx = 1 
    SessionDuration = 2
    MaxTimeSpentInSite = 3

class dLabel:
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
    
#TBD 'InDegree' ,'OutDegree' ,'InRiskDegree' , 'OutRiskDegree' IN SITES POV   

      
class Functions(object):
    
    '''
    '''
    
    def sortFile(self, lines):
        '''Sorts the whole file by User Id, Session Id and Time stamp    '''
        return sorted(lines, key = itemgetter(Label.uId, Label.bSesId, Label.TS))
    
    def createDataContainersForUserAggregationProcess(self):
        
        global users; users = defaultdict(list)
        global sessions; sessions = defaultdict(list)
        global usersActDis; usersActDis = defaultdict(list)
        global usersIP; usersIP = defaultdict(lambda: defaultdict(list))
            
        return
    
    def exportUsersDictToFile(self,fn):
        global users
        usersRiskRankDict = {}
        for u in users:
            usersRiskRankDict[u] = users[u][uLabel.isRisky]
        gm.saveDict(fn, usersRiskRankDict)
        return
    
    def createDataContainersForDomainAggregationProcess(self):
        
        global domains; domains = defaultdict(list)
        global domainsUsers; domainsUsers = defaultdict(lambda: defaultdict(list))
        global domainsRedirections; domainsRedirections = defaultdict (lambda: defaultdict(lambda: defaultdict(list)))
    
        return
          
    def initNewUser(self, userID):
        
        global users; global usersActDis; global usersIP;
        
        # Initialize container with 0 
        for i in [column1 for column1 in dir(uLabel) if not callable(column1) and not column1.startswith("__")]:
            users[userID].append(0)
        
        for j in [column2 for column2 in dir(uDayLabel) if not callable(column2) and not column2.startswith("__")]: 
            usersActDis[userID].append(0)
        
        usersIP[userID] = []
       
        return
    
    def initNewSession(self,sessionID, userID):
        
        global sessions;global sLabel;
        # Initialize with 0 
        for i in [column for column in dir(sLabel) if not callable(column) and not column.startswith("__")]:
        
            sessions[str(sessionID)].append(0)

        sessions[sessionID][sLabel.UserId]
        sessions[sessionID][sLabel.UserId] = userID
        return
    
    def initNewDomain(self, domain, userID):
        
        global domains; global domainsUsers;
        
        # Initialize with 0 
        for column in dir(dLabel):
            domains[domain].append(0)
        
        domainsUsers[domain] = {userID: 0} 
       
        return
    
    def initNewUserInDomain(self, domain, userID):
        '''
        Case when the Domain already exists but that's a visit of a new user
        '''
        global domainsUsers;
        domainsUsers[domain][userID] = 0
       
        return
    
    def initNewRedirectionInDomain(self, domain, redirectedDomain, redirectedUrl):
        '''
        Case when the Domain already exists but that's a visit of a new user
        '''
        global domainsRedirections;
        if (domain not in domainsRedirections): domainsRedirections[domain] = {redirectedDomain: {redirectedUrl: 0}}    # The domain is new
        elif(redirectedDomain not in domainsRedirections[domain]): domainsRedirections[domain][redirectedDomain] = {redirectedUrl: 0}    # The redirectedDomain is new
        else: domainsRedirections[domain][redirectedDomain][redirectedUrl] = 0      # Only the redirectedUrl is new 
    
        return
        
    def handelSessionsAndUserDataAggregation(self):

                
        global l
        
        l.lines = Functions.sortFile(self, l.lines)
        
        Functions.generateAggregativeDataUponSessionSegmentaion(self) # Updates lines[] with generated session and calcs time spent
        
        return None
    
    def handelSessionsAndUserDataAggregation_domainsGraph(self,user_risk_out_file):
        global l 
        l.lines = Functions.sortFile(self, l.lines)
        Functions.generateAggregativeDataUponSessionSegmentaion_domainsGraph(self) # Updates lines[] with generated session and calcs time spent
        
        
        #self.exportUsersDictToFile(filePath)
        trxFunctionsClass.addPervDomain()
        trxFunctionsClass.addRiskRank()
        trxFunctionsClass.addPrevSiteRiskRank()
        trxFunctionsClass.add_redirect_domain_and_riskRank()
        # create users risk dict and write it to file:
        self.exportMyUserRiskLabelDictToFile(user_risk_out_file)
        
        
        return None
    
    def exportMyUserRiskLabelDictToFile(self,fn):
        global l
        mal_weight = trxFunctionsClass.w['mal'] #1
        userRiskDict = {}
        
        for line in l.lines:
            uId = line[Label.uId]
            pRisk = line[Label.prevDomainRiskRank]  # previous URL domain risk rank
            cRisk = line[Label.riskRank]            # current (requested) URL domain risk rank
            rRisk = line[Label.RedirDomainRiskRank] # redirect to URL domain risk rank
            
            if uId in userRiskDict:
                userRiskDict[uId]['risk sum'] += max(pRisk, cRisk, rRisk)
            else:   #new user
                userRiskDict.setdefault(uId,{'risk sum':max(pRisk, cRisk, rRisk), 'visited malware':0})
                #userRiskDict[uId]['risk sum'] = max(line[Label.prevDomainRiskRank] ,line[Label.riskRank])
                #userRiskDict[uId]['visited malware'] = 0
                
            if max(pRisk, cRisk, rRisk) == mal_weight:
                    userRiskDict[uId]['visited malware'] = 1
            
        # if the sum of the risk rank of the domains the user visited is greater than 3
        # or if he visited a known malicious site he'll be defined as a bad user:
        for u in userRiskDict:
            if userRiskDict[u]['visited malware'] or userRiskDict[u]['risk sum'] >= 3:
                userRiskDict[u] = 1
            else:
                userRiskDict[u] = 0
            '''if uId in userRiskDict:
                userRiskDict[uId] += max(line[Label.prevDomainRiskRank] ,line[Label.riskRank])
            else:
                userRiskDict[uId] = max(line[Label.prevDomainRiskRank] ,line[Label.riskRank])
        
        # if the sum of the risk rank of the domains the user visited is greater than 1 it is a bad user:
        for u in userRiskDict:
            if userRiskDict[u] >= 1:
                userRiskDict[u] = 1
            else:
                userRiskDict[u] = 0'''
                
        gm.saveDict(fn, userRiskDict)
        return         
        
    def generateAggregativeDataUponSessionSegmentaion(self):   
        
        '''
        Calculates aggregative values per session and per user
        Generates for each row: New Session by the transactions Time Stamp, The Time Spent in the site
        '''
        
        global timeOut
        global users; global sessions;
        tmpFirstSessionInd = 0 # temporary var indicates the index for first row in the current session
        rowNum = 0   # The line iterator - represents the current row
        lastRowFlag = 0 # Flag is on if this is the last row in the file
        sessionId = 1 # think about unique session id!!!!! TBD random session generator
        countryIds = []
        
        for i in l.lines:  
            currUserId = i[Label.uId]; currBSessionId = i[Label.bSesId]; currTS = i[Label.TS]; countryId = i[Label.countryId]; day = i[Label.dayInWeek]; partOfDay = i[Label.partOfDay]; isRisky = i[Label.isRisky]; ip = i[Label.IP]
                                
            if rowNum < len(l.lines)-1:
                 
                nxtRow = l.lines[rowNum + 1]                
                nxtUserId = nxtRow[Label.uId]; nxtBSessionId = nxtRow[Label.bSesId]; nxtTS = nxtRow[Label.TS]
                
            else:       #This is the last row in the file
                nxtRow = i
                lastRowFlag = 1
            
            # Update the line with the new column: new GENEREATED SESSION id    
            l.lines[rowNum] += [currBSessionId + '#' + str(sessionId)]
            # Update the line with the new column: shouldProcess- if the requested site domain is not web search engine/ social net etc.
            l.lines[rowNum] +=  [Functions.shouldProcessLine(self,i[Label.reqSite])]
            
            generatedSession = currBSessionId + '#' + str(sessionId)
            if generatedSession not in sessions: # Updating the Sessions Container with distinct session ids
                Functions.initNewSession(self, generatedSession, currUserId)
            
            if countryId not in countryIds:
                countryIds.append(countryId)            
             
            if currUserId not in users: # Updating the Users Container with distinct user ids
                Functions.initNewUser(self, currUserId)
            
            # SPENT TIME CALCULATION:
            if (currUserId == nxtUserId and currBSessionId == nxtBSessionId and not lastRowFlag): #This is the same User and same Browser Session
            
                if ((float(nxtTS) - float(currTS)) > timeOut ):       #If the next transaction happened after the session timeout and this is not the last row in the file- we get a NEW sessionId
     
                    Functions.calcTimeSpent(self,tmpFirstSessionInd,rowNum)
                    # Updating the Aggregative data
                    duration = float(l.lines[rowNum][Label.TS])-float(l.lines[tmpFirstSessionInd][Label.TS])
                    trxCounter = rowNum - tmpFirstSessionInd + 1
                    
                    Functions.updateContainersValue(self, 'session', generatedSession, sLabel.SessionDuration, duration)
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalSessionDuration, duration)
                    Functions.updateContainersValue(self, 'session', generatedSession, sLabel.NumOfTrx, trxCounter)
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalNumOfTrx, trxCounter)
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.NumOfSessions, 1)
                    Functions.updateContainersMaxValue(self, 'user', currUserId, uLabel.MaxTimeSpentInSites, sessions[generatedSession][sLabel.MaxTimeSpentInSite])
                    
                    Functions.updateUsersActivityDisterbution(self, currUserId, day, partOfDay, isRisky)
                    Functions.calcNumOfDistinctIPs(self, currUserId, ip)
                    
                    sessionId += 1 # incrementing the session id
                    tmpFirstSessionInd = rowNum + 1
                else:
                    Functions.updateUsersActivityDisterbution(self, currUserId, day, partOfDay, isRisky)
                    Functions.calcNumOfDistinctIPs(self, currUserId, ip)
                    
            
            else: # Not the same User OR not the same Browser Session anymore!
                
                Functions.calcTimeSpent(self,tmpFirstSessionInd,rowNum)
                
                # Updating the Aggregative data
                duration = float(l.lines[rowNum][Label.TS])-float(l.lines[tmpFirstSessionInd][Label.TS])
                trxCounter = rowNum - tmpFirstSessionInd +1
                
                Functions.updateContainersValue(self, 'session', generatedSession, sLabel.SessionDuration, duration)
                Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalSessionDuration, duration)
                Functions.updateContainersValue(self, 'session', generatedSession, sLabel.NumOfTrx, trxCounter) #redirect click shouldn't be counted?
                Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalNumOfTrx, trxCounter)
                Functions.updateContainersValue(self, 'user', currUserId, uLabel.NumOfSessions, 1)
                Functions.updateContainersMaxValue(self, 'user', currUserId, uLabel.MaxTimeSpentInSites, sessions[generatedSession][sLabel.MaxTimeSpentInSite])
                
                Functions.updateUsersActivityDisterbution(self, currUserId, day, partOfDay, isRisky)
                Functions.calcNumOfDistinctIPs(self, currUserId, ip)
                
                if (currUserId != nxtUserId or lastRowFlag): # Before moving on to next user
                    # Total and Avg Aggregation values per User
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalNumOfCountries, len(countryIds))
                    countryIds = [] # Clean the list cause the next trx is a different  user
                    
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.AvgSessionDuration, uLabel.TotalSessionDuration, uLabel.NumOfSessions)
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.AvgTimeSpentInSites, uLabel.TotalSessionDuration, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.AvgTrxInSession, uLabel.TotalNumOfTrx, uLabel.NumOfSessions)
                    #Functions.updateContainersAvgValue(self, 'user', currUserId, 'AvgCountries', 'TotalNumOfCountries', 'NumOfSessions')
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.BadActivityVolPct, uLabel.TotalNumOfRiskyTrx, uLabel.TotalNumOfTrx)
                    
                    # Activity Pct per Part Of The Day
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.MorningActivityPct, uDayLabel.MorningTotalActivity, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.NoonActivityPct, uDayLabel.NoonTotalActivity, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.EveningActivityPct, uDayLabel.EveningTotalActivity, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.NightActivityPct, uDayLabel.NightTotalActivity, uLabel.TotalNumOfTrx)
                 
                    # Risky Activity Pct per Part Of The Day
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.MorningRiskyActivityPct, uDayLabel.MorningTotalRiskyActivity, uDayLabel.MorningTotalActivity)
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.NoonRiskyActivityPct, uDayLabel.NoonTotalRiskyActivity, uDayLabel.NoonTotalActivity)
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.EveningRiskyActivityPct, uDayLabel.EveningTotalRiskyActivity, uDayLabel.EveningTotalActivity)
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.NightRiskyActivityPct, uDayLabel.NightTotalRiskyActivity, uDayLabel.NightTotalActivity)
                    
                    Functions.updateDayWithMaxVol(self, currUserId)
                    Functions.updateNumOfDistinctIPs(self, currUserId)
                    
                                                           
                sessionId += 1 # incrementing the session id
                tmpFirstSessionInd = rowNum + 1
                    
            rowNum += 1
            Functions.evaluteUserRiskLevel(self, i)
             
        return None     
    
    def generateAggregativeDataUponSessionSegmentaion_domainsGraph(self):   
        # THIS FUNC IS WRONG!!! GIVES EVERY ROW A NEW GSNERATED SESSION ID EVEN IF ITS THE SAME SESSION!!!!
        # SHOULD BE FIXED!!!!
        '''
        Calculates aggregative values per session and per user
        Generates for each row: New Session by the transactions Time Stamp, The Time Spent in the site
        '''
        
        global timeOut
        global users; global sessions;
        tmpFirstSessionInd = 0 # temporary var indicates the index for first row in the current session
        rowNum = 0   # The line iterator - represents the current row
        lastRowFlag = 0 # Flag is on if this is the last row in the file
        sessionId = 1 # think about unique session id!!!!! TBD random session generator
        #countryIds = []
        
        for i in l.lines:  
            currUserId = i[Label.uId]; currBSessionId = i[Label.bSesId]; currTS = i[Label.TS]; isRisky = i[Label.isRisky]
            #countryId = i[Label.countryId]; day = i[Label.dayInWeek]; partOfDay = i[Label.partOfDay]; ip = i[Label.IP]
                                           
            if rowNum < len(l.lines)-1:
                 
                nxtRow = l.lines[rowNum + 1]                
                nxtUserId = nxtRow[Label.uId]; nxtBSessionId = nxtRow[Label.bSesId]; nxtTS = nxtRow[Label.TS]
                
            else:       #This is the last row in the file
                nxtRow = i
                lastRowFlag = 1
            
            # Update the line with the new column: new GENEREATED SESSION id    
            l.lines[rowNum] += [currBSessionId + '#' + str(sessionId)]
            # Update the line with the new column: shouldProcess- if the requested site domain is not web search engine/ social net etc.
            l.lines[rowNum] +=  [Functions.shouldProcessLine(self,i[Label.reqSite])]
            
            generatedSession = currBSessionId + '#' + str(sessionId)
            if generatedSession not in sessions: # Updating the Sessions Container with distinct session ids
                Functions.initNewSession(self, generatedSession, currUserId)
            
            #if countryId not in countryIds:
            #    countryIds.append(countryId)            
             
            if currUserId not in users: # Updating the Users Container with distinct user ids
                Functions.initNewUser(self, currUserId)
            # MICHAL ADDED- UPDATE USERS RISK:
            Functions.updateContainersMaxValue(self, 'user', currUserId, uLabel.isRisky, isRisky) 

            ##########NOTE: WHEN ADDING THE calcTimeSpent THE BELOW SHOULD BE DELETED!!!!##########
            l.lines[rowNum] += '0' # Initialize the Time Spent to be Zero! At l.lines[currIdx][16] (position 16)    #TBD- check if can handle l.lines[currIdx] += 0 or convert to int later
            #lines[rowNum][Label.timeSpent] = 0
            l.lines[rowNum] += '0' # The current transaction Does not have Children!
            ##########
            
            # SPENT TIME CALCULATION:
            if (currUserId == nxtUserId and currBSessionId == nxtBSessionId and not lastRowFlag): #This is the same User and same Browser Session
            
                if ((float(nxtTS) - float(currTS)) > timeOut ):       #If the next transaction happened after the session timeout and this is not the last row in the file- we get a NEW sessionId
     
                    ##########NOTE: JUST FOR NOW_ TILLTHE TS WILL BE INCLUDED IN THE GRAPH!!!##########
                    #Functions.calcTimeSpent(self,tmpFirstSessionInd,rowNum)
                    
                    # Updating the Aggregative data
                    duration = float(l.lines[rowNum][Label.TS])-float(l.lines[tmpFirstSessionInd][Label.TS])
                    trxCounter = rowNum - tmpFirstSessionInd + 1
                    '''
                    Functions.updateContainersValue(self, 'session', generatedSession, sLabel.SessionDuration, duration)
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalSessionDuration, duration)
                    Functions.updateContainersValue(self, 'session', generatedSession, sLabel.NumOfTrx, trxCounter)
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalNumOfTrx, trxCounter)
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.NumOfSessions, 1)
                    Functions.updateContainersMaxValue(self, 'user', currUserId, uLabel.MaxTimeSpentInSites, sessions[generatedSession][sLabel.MaxTimeSpentInSite])
                    
                    Functions.updateUsersActivityDisterbution(self, currUserId, day, partOfDay, isRisky)
                    Functions.calcNumOfDistinctIPs(self, currUserId, ip)
                    '''
                    sessionId += 1 # incrementing the session id
                    tmpFirstSessionInd = rowNum + 1
                '''
                else:
                    Functions.updateUsersActivityDisterbution(self, currUserId, day, partOfDay, isRisky)
                    Functions.calcNumOfDistinctIPs(self, currUserId, ip)
                '''   
            
            else: # Not the same User OR not the same Browser Session anymore!
                
                ##########NOTE: JUST FOR NOW_ TILLTHE TS WILL BE INCLUDED IN THE GRAPH!!!##########
                #Functions.calcTimeSpent(self,tmpFirstSessionInd,rowNum)
                
                # Updating the Aggregative data
                duration = float(l.lines[rowNum][Label.TS])-float(l.lines[tmpFirstSessionInd][Label.TS])
                trxCounter = rowNum - tmpFirstSessionInd +1
                '''
                Functions.updateContainersValue(self, 'session', generatedSession, sLabel.SessionDuration, duration)
                Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalSessionDuration, duration)
                Functions.updateContainersValue(self, 'session', generatedSession, sLabel.NumOfTrx, trxCounter) #redirect click shouldn't be counted?
                Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalNumOfTrx, trxCounter)
                Functions.updateContainersValue(self, 'user', currUserId, uLabel.NumOfSessions, 1)
                Functions.updateContainersMaxValue(self, 'user', currUserId, uLabel.MaxTimeSpentInSites, sessions[generatedSession][sLabel.MaxTimeSpentInSite])
                
                Functions.updateUsersActivityDisterbution(self, currUserId, day, partOfDay, isRisky)
                Functions.calcNumOfDistinctIPs(self, currUserId, ip)
                
                if (currUserId != nxtUserId or lastRowFlag): # Before moving on to next user
                    # Total and Avg Aggregation values per User
                    Functions.updateContainersValue(self, 'user', currUserId, uLabel.TotalNumOfCountries, len(countryIds))
                    countryIds = [] # Clean the list cause the next trx is a different  user
                    
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.AvgSessionDuration, uLabel.TotalSessionDuration, uLabel.NumOfSessions)
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.AvgTimeSpentInSites, uLabel.TotalSessionDuration, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.AvgTrxInSession, uLabel.TotalNumOfTrx, uLabel.NumOfSessions)
                    #Functions.updateContainersAvgValue(self, 'user', currUserId, 'AvgCountries', 'TotalNumOfCountries', 'NumOfSessions')
                    Functions.updateContainersAvgValue(self, 'user', currUserId, uLabel.BadActivityVolPct, uLabel.TotalNumOfRiskyTrx, uLabel.TotalNumOfTrx)
                    
                    # Activity Pct per Part Of The Day
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.MorningActivityPct, uDayLabel.MorningTotalActivity, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.NoonActivityPct, uDayLabel.NoonTotalActivity, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.EveningActivityPct, uDayLabel.EveningTotalActivity, uLabel.TotalNumOfTrx)
                    Functions.updateContainersAvgValue(self, 'userDisAct1', currUserId, uLabel.NightActivityPct, uDayLabel.NightTotalActivity, uLabel.TotalNumOfTrx)
                 
                    # Risky Activity Pct per Part Of The Day
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.MorningRiskyActivityPct, uDayLabel.MorningTotalRiskyActivity, uDayLabel.MorningTotalActivity)
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.NoonRiskyActivityPct, uDayLabel.NoonTotalRiskyActivity, uDayLabel.NoonTotalActivity)
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.EveningRiskyActivityPct, uDayLabel.EveningTotalRiskyActivity, uDayLabel.EveningTotalActivity)
                    Functions.updateContainersAvgValue(self, 'userDisAct2', currUserId, uLabel.NightRiskyActivityPct, uDayLabel.NightTotalRiskyActivity, uDayLabel.NightTotalActivity)
                    
                    Functions.updateDayWithMaxVol(self, currUserId)
                    Functions.updateNumOfDistinctIPs(self, currUserId)
                    
                '''                                           
                sessionId += 1 # incrementing the session id
                tmpFirstSessionInd = rowNum + 1
                    
            rowNum += 1
            #Functions.evaluteUserRiskLevel(self, i)
        #DEBUG: print "users container:    "; print users     
        return None  

    def calcTimeSpent(self, firstRow, lastRow):   
        '''
            Time Spent Approximation for each transaction
            Calculates "Max Time Spent In Site" per session
            the firstRow and lastRow represents the row index of the generated session in lines[]
        '''
        global l
            
        for i in l.lines[firstRow:lastRow + 1] :
            
            currIdx = l.lines.index(i)
            l.lines[currIdx] += '0' # Initialize the Time Spent to be Zero! At lines[currIdx][16] (position 16)    #TBD- check if can handle lines[currIdx] += 0 or convert to int later
            l.lines[currIdx] += '0' # The current transaction Does not have Children!
            
            if (currIdx != lastRow and i[Label.shouldProcess]): # If not end of generated session (we cannot calculate the spent time for the last row) and this line should be processed
                nxtIdx = currIdx + 1
                       
                for j in l.lines[nxtIdx:lastRow + 1]:
                    if (i[Label.reqSite] == j[Label.prevSite]):  
                        
                        #lines[currIdx][Label.timeSpent] = str(int(round(float(j[Label.TS]) - float(i[Label.TS])))) # Update Time Spent- ROUNDED!!!-
                        l.lines[currIdx][Label.timeSpent] = int(round(float(j[Label.TS]) - float(i[Label.TS]))) # Update Time Spent- ROUNDED!!!-
                        break
                
                if (l.lines[currIdx][Label.timeSpent] == '0'):    #The current row has no children, hence we define the spent time as the gap till the next trx of the session.
                    
                    #lines[currIdx][Label.timeSpent] = str(int(round(float(lines[nxtIdx][Label.TS]) - float(lines[currIdx][Label.TS])))) #Update Time Spent by the next trx- ROUNDED!!!
                    l.lines[currIdx][Label.timeSpent] = int(round(float(l.lines[nxtIdx][Label.TS]) - float(l.lines[currIdx][Label.TS]))) #Update Time Spent by the next trx- ROUNDED!!!
                
                Functions.updateContainersMaxValue(self, 'session', i[Label.genSesId], sLabel.MaxTimeSpentInSite, l.lines[currIdx][Label.timeSpent])
            
        return None
    
    def updateHashedContainersValue(self, key1, key2, value):
        
        global domainsUsers
        domainsUsers[key1][key2] += value
            
        return
    
    def updateTripleHashedContainersValue(self, key1, key2, key3, value):
        
        global domainsRidirections
        domainsRedirections[key1][key2][key3] += value
            
        return
    
    def updateContainersValue(self, type, key, column, value):
        
        if (type == 'session'):
            global sessions
            sessions[key][column] += value
        
        if (type == 'user'):
            global users
            users[key][column] += value
        
        if (type == 'domain'):
            global domains
            domains[key][column] += value
            
        return
    
    def updateContainersMaxValue(self, type, key, column, value):
        
        if (type == 'session'):
            global sessions
            
            if (sessions[key][column] < value): sessions[key][column] = value 
        
        if (type == 'user'):
            global users
            if (users[key][column] < value): users[key][column] = value 
        
        if (type == 'domain'):
            global domains
            if (domains[key][column] < value): domains[key][column] = value 
        return
    
    def updateContainersAvgValue(self, type, key, column, numerator, denominator):
        
        if (type == 'userDisAct1' or type == 'userDisAct2' or type == 'user'):
            global users
            global usersActDis 
            
            if (type == 'userDisAct1'):
                users[key][column] = usersActDis[key][numerator] / float(users[key][denominator])
                
            if (type == 'userDisAct2'):
                 
                if (usersActDis[key][denominator] != 0):
                    users[key][column] = usersActDis[key][numerator] / float(usersActDis[key][denominator])
            
            if (type == 'user'):    
                users[key][column] = users[key][numerator] / float(users[key][denominator])
                        
        if (type == 'domain'):
            global domains
            domains[key][column] = domains[key][numerator] / float(domains[key][denominator])
 
        return
    
    def evaluteUserRiskLevel(self, userTrx):
        
        global users
        userID = userTrx[Label.uId]
        # Check if the current transaction of this user is Risky, 
        # If does, mark him as isRisky in the Users Container
        if(userTrx[Label.isRisky] == 1):
            
            Functions.updateContainersValue(self, 'user', userID, uLabel.TotalNumOfRiskyTrx, 1)
        
            if (userTrx[Label.malRisk] == 1 and users[userID][uLabel.malRisk] == 0):
                users[userID][uLabel.malRisk] = 1
            if (userTrx[Label.copyrightRisk] == 1 and users[userID][uLabel.copyrightRisk] == 0):
                users[userID][uLabel.copyrightRisk] = 1
            if (userTrx[Label.keywordRisk] == 1 and users[userID][uLabel.keywordRisk] == 0):
                users[userID][uLabel.keywordRisk] = 1
            if (userTrx[Label.isRisky] == 1 and users[userID][uLabel.isRisky] == 0):
                users[userID][uLabel.isRisky] = 1
            
        
        return
    
    def updateDayWithMaxVol(self, userId):
        global users; 
        global usersActDis
        days = sorted(
                      [
                       ('Sunday',  usersActDis[userId][uDayLabel.SundayTrx]), 
                       ('Monday', usersActDis[userId][uDayLabel.MondayTrx]), 
                       ('Tuesday' , usersActDis[userId][uDayLabel.TuesdayTrx]), 
                       ('Wednesday' , usersActDis[userId][uDayLabel.WednesdayTrx]), 
                       ('Thursday' , usersActDis[userId][uDayLabel.ThursdayTrx]), 
                       ('Friday', usersActDis[userId][uDayLabel.FridayTrx]), 
                       ('Saturday' ,usersActDis[userId][uDayLabel.SaturdayTrx])
                        ]
                        , key=itemgetter(1), reverse = True)
        users[userId][uLabel.DayInWeek] = days[0][0]
        users[userId][uLabel.IsWeekend] = trxFunctionsClass.getWeekend(days[0][0]) 
         
        return
    
    def updateDaysActivityDisterbution(self, userId, day):
        
        global usersActDis
        
        if (day == 'Sunday'):
            usersActDis[userId][uDayLabel.SundayTrx] += 1
        if (day == 'Monday'):
            usersActDis[userId][uDayLabel.MondayTrx] += 1
        if (day == 'Tuesday'):
            usersActDis[userId][uDayLabel.TuesdayTrx] += 1
        if (day == 'Wednesday'):
            usersActDis[userId][uDayLabel.WednesdayTrx] += 1
        if (day == 'Thursday'):
            usersActDis[userId][uDayLabel.ThursdayTrx] += 1
        if (day == 'Friday'):
            usersActDis[userId][uDayLabel.FridayTrx] += 1
        if (day == 'Saturday'):
            usersActDis[userId][uDayLabel.SaturdayTrx] += 1
        
        return
    
    def updatePartOfDayActivityDisterbution(self, userId, partOfDay, isRisky):
        
        global usersActDis
        
        if (partOfDay == 'Morning'):
            usersActDis[userId][uDayLabel.MorningTotalActivity] += 1
            if (isRisky == 1):
                usersActDis[userId][uDayLabel.MorningTotalRiskyActivity] += 1
        if (partOfDay == 'Noon'):
            usersActDis[userId][uDayLabel.NoonTotalActivity] += 1
            if (isRisky == 1):
                usersActDis[userId][uDayLabel.NoonTotalRiskyActivity] += 1
        if (partOfDay == 'Evening'):
            usersActDis[userId][uDayLabel.EveningTotalActivity] += 1
            if (isRisky == 1):
                usersActDis[userId][uDayLabel.EveningTotalRiskyActivity] += 1
        if (partOfDay == 'Night'):
            usersActDis[userId][uDayLabel.NightTotalActivity] += 1
            if (isRisky == 1):
                usersActDis[userId][uDayLabel.NightTotalRiskyActivity] += 1
        return
    
    def updateUsersActivityDisterbution(self, userId, day, partOfDay, isRisky):
        
        Functions.updateDaysActivityDisterbution(self, userId, day)
        Functions.updatePartOfDayActivityDisterbution(self, userId, partOfDay, isRisky)
        return
    
    def calcNumOfDistinctIPs(self, userId, ip):
        
        if ip not in usersIP[userId]:
            usersIP[userId].append(ip)
        return
    
    def updateNumOfDistinctIPs(self, userId):
        Functions.updateContainersValue(self, 'user', userId, uLabel.NumOfDistinctIPs, len(usersIP[userId]))
        return

# THE BELOW METHOD CHANGED!!!!!!!!!!         
    def shouldProcessLine(self, url): 
        '''
        This method gets the requested URL as input and checks if its domain is one of the popular web search engines/ social networks etc.
        We do not interest in such domains, hence those transactions should not be further processed, means- return False.
        Otherwise returns True (should be processed)
        
        reqSiteDomain = ''#getDomainFromRequestedSite(url)
        if (reqSiteDomain is not None):
            NotRelevant = re.compile('\.facebook\.com|\.amazon\.com|instagram\.com|\.wikipedia\.|\.youtube\.com|\.vk\.com|\.ebay\.com|\.linkedin\.com|twitter\.com|\.pinterest\.com|myspace\.com|\.deviantart\.com|\.livejournal\.com|\.tagged\.com|\.orkut\.com|\.ning\.com|\.meetup\.com', re.IGNORECASE).search(reqSiteDomain)   #TBD- we might consider extracting the domain HERE before the session !!
            if (NotRelevant is None): return True       #The URL should be processed
        return False
        '''
        reqSiteDomain = trxFunctionsClass.getDomainFromRequestedSite(url)
        if (reqSiteDomain != '' ): return 1 #getDomainFromRequestedSite returns '' if failed
        return 0
    
    def handelDomainDataAggregation(self):
        self.createDataContainersForDomainAggregationProcess()
        global l, domains, G
        
            
        for line in l.lines:
            #print "------------------------------------------------------------------------"
            #print line
            userId = line[Label.uId]
            domain = line[Label.domain]
            #print "domain: " + domain
            prevDomain = line[Label.prevSite]
            isLink = int(line[Label.isLink])
            #if (line[Label.isLink]): print "isLink: " +line[Label.isLink];print "ref: " + line[Label.httpRefer]; prevDomain = line[Label.prevSite]
            #print "prevDomain: " + str(prevDomain) + ",    isLink: " + str(isLink)
            isRisky = line[Label.isRisky]
            httpCode = line[Label.httpCode]
            timeSpent = float(line[Label.timeSpent]) 
            
            '''#  MICHAL NEW:
            if(line[Label.shouldProcess]):
                G.handleLine(line, users[userId][uLabel.isRisky])'''
            
            # MICHAL old:
            if(line[Label.shouldProcess]):
                if domain not in domains: 
                    Functions.initNewDomain(self, domain, userId)   # Updating the Domains Container with distinct domains
                    #dGraphClass.addNode(domain)                     # Updating the graph with distinct domains
                    #print "new domain!"
                
                # If coming from prevSite update the graph accordingly:
                if (prevDomain):    #if prevDomain is not zero, as initialized
                #if (prevDomain != ''):
                    pDomain = trxFunctionsClass.getDomainFromRequestedSite(prevDomain)
                    #print "prevDomain exist! pDomain: " + pDomain
                    if pDomain not in domains:
                        Functions.initNewDomain(self, pDomain, userId)   # Updating the Domains Container with distinct domains

                        #dGraphClass.addNode(pDomain)
                        #print "new pDomain! pDomain: " + pDomain
                    #dGraphClass.addEdge(pDomain, domain)
                
                #print "out degree: " + str(dGraphObj.out_degree(domain))
                Functions.updateDomainUsersAggData(self, line)
                Functions.updateContainersMaxValue(self, 'domain', domain, dLabel.IsInBlackList, isRisky) 
    
                
                # If the current line httpCode starts with 3XX- update domainsRedirections container accordingly
                if (httpCode.startswith('3')):
                    Functions.updateContainersValue(self, 'domain', domain, dLabel.TotalNumOfRedirections, 1)
                    Functions.updateDomainRedirectAggData(self, line)
                   
                Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfVisits, 1)
                Functions.updateContainersValue(self, 'domain', domain, dLabel.TotalTimeSpent, timeSpent)    
                Functions.updateContainersMaxValue(self, 'domain', domain, dLabel.MaxTimeSpent, timeSpent)    
                
            
           
        # After going over all "lines", starting to calculate the aggregative data upon domains container
        Functions.updateDomainAggData(self)
        ''''G.updateGraphAggData()
        G.graphPlot('/home/michal/Desktop/graphPlots/graph_part3.png')
        
        dGraphClass.runPageRank()
        #DEBUG: dGraphClass.printGraphAttr('node'); dGraphClass.printGraphAttr('edge')
        '''
        domains_dict_file='/home/michal/SALSA_files/tmp/domains_dict.csv'
        gm.saveDict(domains_dict_file, domains)
        return
    
    def handelDomainDataAggregation_domainsGraph(self,outputFile):
        
        global l; global G
        #global domains;
            
        for line in l.lines:
            #print "------------------------------------------------------------------------"
            #print line
            userId = line[Label.uId]
            #domain = line[Label.domain]
            #print "domain: " + domain
            #prevDomain = line[Label.prevSite]
            #isLink = int(line[Label.isLink])
            #if (line[Label.isLink]): print "isLink: " +line[Label.isLink];print "ref: " + line[Label.httpRefer]; prevDomain = line[Label.prevSite]
            #print "prevDomain: " + str(prevDomain) + ",    isLink: " + str(isLink)
            #isRisky = line[Label.isRisky]
            #httpCode = line[Label.httpCode]
            #timeSpent = float(line[Label.timeSpent]) 
            
            #  MICHAL NEW:
            if(line[Label.shouldProcess]):
                G.handleLine(line, users[userId][uLabel.isRisky])
            '''
            # MICHAL old:
            if domain not in domains: 
                Functions.initNewDomain(self, domain, userId)   # Updating the Domains Container with distinct domains
                #dGraphClass.addNode(domain)                     # Updating the graph with distinct domains
                #print "new domain!"
            
            # If coming from prevSite update the graph accordingly:
            #if (prevDomain):    #if prevDomain is not zero, as initialized
            #if (prevDomain != ''):
                #pDomain = TrxFunctionsClass.getDomainFromRequestedSite(prevDomain)
                #print "prevDomain exist! pDomain: " + pDomain
                #if pDomain not in domains:
                    #dGraphClass.addNode(pDomain)
                    #print "new pDomain! pDomain: " + pDomain
                #dGraphClass.addEdge(pDomain, domain)
            
            #print "out degree: " + str(dGraphObj.out_degree(domain))
            Functions.updateDomainUsersAggData(self, line)
            Functions.updateContainersMaxValue(self, 'domain', domain, dLabel.IsInBlackList, isRisky) 
            
            
            # If the current line httpCode starts with 3XX- update domainsRedirections container accordingly
            if (httpCode.startswith('3')):
                Functions.updateContainersValue(self, 'domain', domain, dLabel.TotalNumOfRedirections, 1)
                Functions.updateDomainRedirectAggData(self, line)
               
            Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfVisits, 1)
            Functions.updateContainersValue(self, 'domain', domain, dLabel.TotalTimeSpent, timeSpent)    
            Functions.updateContainersMaxValue(self, 'domain', domain, dLabel.MaxTimeSpent, timeSpent)    
            '''
            
           
        # After going over all "lines", starting to calculate the aggregative data upon domains container
        #Functions.updateDomainAggData(self)
        G.updateGraphAggData()
        # DEBUG: dGraphClass.graphPlot(dGraphObj, "/home/michal/Desktop/graphPlots/graph_part3.png")
        
        #dGraphClass.runPageRank(outputFile)
        graph_as_dict_file='/home/michal/SALSA_files/tmp/graph_as_dict_of_dicts.csv'
        G.writeGraphToFile(graph_as_dict_file)
        
        '''    DEBUG
        dGraphClass.printGraphAttr('node')
        dGraphClass.printGraphAttr('edge')
        '''
        return

    def updateDomainRedirectAggData(self, trx):
        
        domain = trx[Label.domain]
        redirectToUrl = trx[Label.httpRedirectToUrl]
        redirectToDomain = trxFunctionsClass.getDomainFromRequestedSite(redirectToUrl)
        
        # Update domainsRedirections container in case of new domain or redirected domain/URL:
        if((domain not in domainsRedirections) or (redirectToDomain not in domainsRedirections[domain]) or (redirectToUrl not in domainsRedirections[domain][redirectToDomain])):  
            Functions.initNewRedirectionInDomain(self, domain, redirectToDomain, redirectToUrl)
        
        # Update domainsRedirections Container with number of redirection to the specific redirected URL
        Functions.updateTripleHashedContainersValue(self, domain, redirectToDomain, redirectToUrl, 1 )

        return
    
    def updateDomainUsersAggData(self, trx):
        
        domain = trx[Label.domain]
        userId = trx[Label.uId]
        
        if(userId not in domainsUsers[domain]):
            Functions.initNewUserInDomain(self, domain, userId)
        
        # Update domainsUsers Container with number of visits for the specific userId
        Functions.updateHashedContainersValue(self, domain, userId, 1 )
        
        return
    
    def updateDomainAggData(self):
        
        global users;global domains; global domainsUsers;
                
        for domain in domains:
            domainList = domains[domain]
            
            # Update domains container related to its features
            Functions.updateContainersAvgValue(self, 'domain', domain, dLabel.AvgTimeSpent, dLabel.TotalTimeSpent, dLabel.NumOfVisits)    
            Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfDistinctVisitors, len(domainsUsers[domain]))
            
            
            # Update domains container related to domainUsers container features
            for user in domainsUsers[domain]:
                if (users[user][uLabel.isRisky] == 1):
                    Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfRiskyVisitors, 1)
                    if (users[user][uLabel.malRisk] == 1):
                        Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfMalwareVisitors, 1)
                    if (users[user][uLabel.copyrightRisk] == 1):
                        Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfCopyrightVisitors, 1)
                    if (users[user][uLabel.keywordRisk] == 1):
                        Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfKeywordVisitors, 1)
                        
            Functions.updateContainersAvgValue(self, 'domain', domain, dLabel.UsersInRiskDegree, dLabel.NumOfRiskyVisitors, dLabel.NumOfDistinctVisitors)
            
            
            # Update domains container related to domainRedirects container features
            if domain in domainsRedirections:
                Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfDistinctDomainRedirections, len(domainsRedirections[domain]))  
                
                for redirectedDomain in domainsRedirections[domain]:
                    Functions.updateContainersValue(self, 'domain', domain, dLabel.NumOfDistinctUrlRedirections, len(domainsRedirections[domain][redirectedDomain]))
                
    
        #print users
        #print domains
        #print domainsRedirections
        #print domainsUsers                    
        return   
     
    def writeUserAggregativeData(self, tarPath):
        
        os.path.exists(tarPath) and os.remove(tarPath)
        target = open(tarPath, 'a')
        
        # Add IF with TimeSpentThreshold
        
        for line in users: 
            target.write(line)
            for i in users[line]:
                target.write("\t" + str(i))
            target.write("\n")
        
        target.close()
        
        return
    
    def writeAggregativeDataForWeka(self, tarPath, type):
        
        if (type == 'user'): con = users
        if (type == 'domain'): con = domains
        os.path.exists(tarPath) and os.remove(tarPath)
        target = open(tarPath, 'a')
        
        # Write Header
        header = Functions.generateHeaderForWekaInputFile(self, type)
        target.write(header)
        
        # Add IF with TimeSpentThreshold
        
        for line in con: 
            target.write("'" + line + "'")
            for i in con[line]:
                target.write("," + "'" + str(i) + "'")
            target.write("\n")
        
        target.close()
        
        return
    
    def generateHeaderForWekaInputFile(self, type):
        
        if (type == 'user'):
            relation = 'userAggCyberTrx'
            
            header = (
                    "@RELATION " + relation +
                    "\n @ATTRIBUTE Id string"
                    "\n @ATTRIBUTE NumOfSessions numeric" + 
                    "\n @ATTRIBUTE TotalNumOfTrx numeric" +  
                    "\n @ATTRIBUTE TotalSessionDuration numeric" +
                    "\n @ATTRIBUTE MaxTimeSpentInSites numeric" + 
                    "\n @ATTRIBUTE TotalNumOfCountries numeric" + 
                    "\n @ATTRIBUTE AvgSessionDuration numeric" + 
                    "\n @ATTRIBUTE AvgTimeSpentInSites numeric" + 
                    "\n @ATTRIBUTE AvgTrxInSession numeric" + 
                    #"\n @ATTRIBUTE AvgCountries numeric" +
                    "\n @ATTRIBUTE TotalNumOfRiskyTrx numeric" + 
                    "\n @ATTRIBUTE BadActivityVolPct numeric" +
                    "\n @ATTRIBUTE isRisky {0, 1}" +
                    "\n @ATTRIBUTE malRisk {0, 1}" + 
                    "\n @ATTRIBUTE copyrightRisk {0, 1}" + 
                    "\n @ATTRIBUTE keywordRisk {0, 1}" +
                    "\n @ATTRIBUTE DayInWeek {Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday}" +
                    "\n @ATTRIBUTE IsWeekend numeric" +
                    "\n @ATTRIBUTE CountryId {0, 1}" +
                    "\n @ATTRIBUTE NumOfDistinctIPs numeric" +
                    "\n @ATTRIBUTE MorningActivityPct numeric" +
                    "\n @ATTRIBUTE MorningRiskyActivityPct numeric" +
                    "\n @ATTRIBUTE NoonRiskyActivityPct numeric" +
                    "\n @ATTRIBUTE EveningActivityPct numeric" +
                    "\n @ATTRIBUTE EveningRiskyActivityPct numeric" +
                    "\n @ATTRIBUTE NightActivityPct numeric" +
                    "\n @ATTRIBUTE NightRiskyActivityPct numeric" +
                    "\n@DATA \n \n")
            
           
        if (type == 'domain'):
            relation = 'domainAggCyberTrx'
            
            header = (
                    "@RELATION " + relation +
                    "\n @ATTRIBUTE Domain string"
                    "\n @ATTRIBUTE NumOfVisits numeric" +
                    "\n @ATTRIBUTE NumOfDistinctVisitors numeric" +
                    "\n @ATTRIBUTE NumOfRiskyVisitors numeric" +
                    "\n @ATTRIBUTE NumOfMalwareVisitors numeric" +
                    "\n @ATTRIBUTE NumOfCopyrightVisitors numeric" +
                    "\n @ATTRIBUTE NumOfKeywordVisitors numeric" +
                    "\n @ATTRIBUTE TotalTimeSpent numeric" +
                    "\n @ATTRIBUTE AvgTimeSpent numeric" +
                    "\n @ATTRIBUTE MaxTimeSpent numeric" +
                    "\n @ATTRIBUTE InDegree numeric" +
                    "\n @ATTRIBUTE OutDegree numeric" +
                    "\n @ATTRIBUTE UsersInRiskDegree numeric" +
                    "\n @ATTRIBUTE UsersOutRiskDegree numeric" +
                    "\n @ATTRIBUTE IsInBlackList numeric" +
                    "\n @ATTRIBUTE TotalNumOfRedirections numeric" +
                    "\n @ATTRIBUTE NumOfDistinctUrlRedirections numeric" +
                    "\n @ATTRIBUTE NumOfDistinctDomainRedirections numeric" +
                    "\n@DATA \n \n")
                    
        return header
    
    def importLinesFromFile(self,filePath):
        global l
        l.readListFromFile(filePath)
        return
    
    def exportLinesToFile(self,filePath):
        global l
        l.writeListToFile(filePath)
        return
    

    
        