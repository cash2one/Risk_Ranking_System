#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 20, 2014

@author: michal
'''
#global G
import numpy as np


class myClass():
    member1={}#{'a1':{'b1':{'g':0,'b':1},'b2':{'g':1,'b':1}},'a3':{'b3':{'g':0,'b':0}}}
    member2=[]#[1,2,3,4,5,6]
    
    def set_mem1(self):
        self.member1={'a1':{'b1':{'g':0,'b':1},'b2':{'g':1,'b':1}},'a3':{'b3':{'g':0,'b':0}}}
        return
    def set_mem2(self):
        self.member2=[1,2,3,4,5,6]
        return
    def clear(self):
        self.member1.clear()
        del self.member2[:]
        return
    
G=[1,2,3,4,5,999]
M=myClass()


'''class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            print 'item= '+str(item)+'\tself[item]= '+str(self[item])
            return value

    
a = AutoVivification()

a['a']['1']['g'] = 4
print '------------'
a['a']['2']['b'] = 5
print '------------'
a['a']['1']['b'] = 6
print '------------'
#a['a']['2']['g']
a['a']['2']['g'] +=0

print a'''

'''print '=================='
M = np.matrix([[0,0,1.],[1.,1.,0]])
for x in np.nditer(M,op_flags=['readwrite']):
    x[...] = max(x,0.5)
print M
'''
''''a = np.arange(6).reshape(2,3)
print a
for x in np.nditer(a, op_flags=['readwrite']):
    x[...] = 2 * x
print 'after'; print a'''


