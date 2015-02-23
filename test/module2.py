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
#import pylab as plt
#import pylab as P
   

''''n, bins, patches = P.hist(x, 50, normed=1, histtype='step', cumulative=True)

# add a line showing the expected distribution
y = P.normpdf( bins, mu, sigma).cumsum()
y /= y[-1]
l = P.plot(bins, y, 'k--', linewidth=1.5)

# create a second data-set with a smaller standard deviation
sigma2 = 15.
x = mu + sigma2*P.randn(10000)

n, bins, patches = P.hist(x, bins=bins, normed=1, histtype='step', cumulative=True)

# add a line showing the expected distribution
y = P.normpdf( bins, mu, sigma2).cumsum()
y /= y[-1]
l = P.plot(bins, y, 'r--', linewidth=1.5)

# finally overplot a reverted cumulative histogram
n, bins, patches = P.hist(x, bins=bins, normed=1,
    histtype='step', cumulative=-1)


P.grid(True)
P.ylim(0, 1.05)'''
#----------------------------------
plt.figure(figsize=(12, 14)) 
# These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  

algs = ['test1','test2','test3']
data = [np.array(np.random.rand(1000)),np.array(np.random.rand(1000)),np.array(np.random.rand(1000))]

#y,binEdges=np.histogram(data[0],bins=10)
y, bins, patches = plt.hist(data[0], bins=10, normed=1, histtype='step')#, cumulative=-1)#cumulative=True)
print y;print bins; print patches
data2=np.array(np.random.rand(1000))
#y2=np.histogram(data2,bins=10)[0]
y2, bins, patches = plt.hist(data2, bins=10, normed=1, histtype='step')#, cumulative=-1)
data3=np.array(np.random.rand(1000))
#y3,binEdges=np.histogram(data3,bins=10)
y3, bins, patches = plt.hist(data3, bins=10, normed=1, histtype='step')#, cumulative=-1)
data4=np.array(np.random.rand(1000))
#y4,binEdges=np.histogram(data4,bins=10)
y4, bins, patches = plt.hist(data4, bins=10, normed=1, histtype='step')#, cumulative=-1)

Y = [y,y2,y3,y4]
#bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

'''plt.plot(bincenters,y,'-',lw=2.5, color=tableau20[0], label="test1")
plt.plot(bincenters,y2,'-', lw=2.5, color=tableau20[2], label="test2")
plt.plot(bincenters,y3,'-', lw=2.5, color=tableau20[4], label="test3")
plt.plot(bincenters,y4,'-', lw=2.5, color=tableau20[6], label="test4")
'''
bins_range = bins[:-1]
'''
plt.plot(bins_range,y,'-',lw=2.5, color=tableau20[0], label="test1")
plt.plot(bins_range,y2,'-', lw=2.5, color=tableau20[2], label="test2")
plt.plot(bins_range,y3,'-', lw=2.5, color=tableau20[4], label="test3")
plt.plot(bins_range,y4,'-', lw=2.5, color=tableau20[6], label="test4")
#plt.plot(bincenters,y,'-',bincenters,y2,'r-')
'''

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.), ncol=3,prop={'size':11}, fancybox=True, shadow=True)
plt.grid()


'''ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)  

ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()'''

'''ylim = list(plt.axis())[-2:]
for y in np.arange(ylim[0], ylim[1], 0.005):  
    plt.plot(range(0,10), [y] * 10, "--", lw=0.5, color="black", alpha=0.3)  '''
            
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                labelbottom="on", left="off", right="off", labelleft="on")  

plt.show()


#plt.savefig('bla.png')


'''
x = np.array([1,0,2,0,3,0,4,5,6,7,8])
print np.where(x == 0)[0]
print x[np.where(x == 0)[0]]'''
#p.show()