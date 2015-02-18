#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 20, 2014

@author: michal
'''
#global G
'''import numpy as np


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
'''

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

'''import tldextract, re
url = 'paypal-marketing.co.uk'
print tldextract.extract(url).domain
var = (1,2,3)
var2 = {1,2,3}
var2.update([4,5,3,6])
print var,var2

l1 = [1, 2, 3]
l2 = l1
del l1[:]
print(l1)
url = 'orrenty.com'
risky = re.compile('Torrent|Crack|[^s]Hack|Keygen|1337x|Bitsnoop|Ailbreak|Spyware|Pirate|Astalavista|\
Demonoid|Phrozencrew|Underground|Warez|Btjunkie|H33t|Sex|[^you]Tube|^Tube', re.IGNORECASE).search(url)
print 'risky: ',risky
'''


import numpy as np
#import pylab as p
import matplotlib.pyplot as plt

'''#plt.subplot(110)
plt.plot([1,2,3], label="test1")
plt.plot([3,2,1], label="test2")
# Place a legend to the right of this smaller figure.
plt.legend(bbox_to_anchor=(0.79, 0.98), loc=2, borderaxespad=0.)

plt.show()'''

algs = ['test1','test2','test3']
data = [np.array(np.random.rand(1000)),np.array(np.random.rand(1000)),np.array(np.random.rand(1000))]

binEdges=np.histogram(data[0],bins=10)[1]
print 'binEdges',binEdges, 'type-',type(binEdges)
data2=np.array(np.random.rand(1000))
y2=np.histogram(data2,bins=10)[0]
print type(y2)
'''
data3=np.array(np.random.rand(1000))
y3,binEdges=np.histogram(data3,bins=10)
data4=np.array(np.random.rand(1000))
y4,binEdges=np.histogram(data4,bins=10)'''

bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

print 'bincenters',bincenters,type(bincenters)
#plt.subplot(110)
'''plt.plot(bincenters,y,'-',label="test1")
plt.plot(bincenters,y2,'-', label="test2")
plt.plot(bincenters,y3,'-', label="test3")
plt.plot(bincenters,y4,'-', label="test4")'''
#plt.plot(bincenters,y,'-',bincenters,y2,'r-')

print np.histogram(data[0],bins=10)[0]
print np.histogram(data[1],bins=10)[0]
print np.histogram(data[2],bins=10)[0]

for i in data:
    y,b = np.histogram(data[i],bins=10)#,dtype=int)
    alg = str(algs[i])
    plt.plot(bincenters,y,'-', label=alg)
        

plt.legend(bbox_to_anchor=(0.79, 0.98), loc=2, borderaxespad=0.)

plt.show()


plt.savefig('bla.png')



x = np.array([1,0,2,0,3,0,4,5,6,7,8])
print np.where(x == 0)[0]
print x[np.where(x == 0)[0]]
#p.show()