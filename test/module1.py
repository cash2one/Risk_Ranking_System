'''import graphlab
import generalMethods as gm
#print lg.classify()
f = '/home/michal/SALSA_files/tmp/small_test/domains_risk_dict.csv_head_253_tail_3'
d = gm.readDict(f)
for k in d:
    print k
    #print k.encode("ascii", "ignore").decode("ascii") == k
    try:
        k.decode('ascii')
    except UnicodeDecodeError:
        print "it was not a ascii-encoded unicode string"
    else:
        print "It may have been an ascii-encoded unicode string"
#test_ascii = lambda s: all(c < u'\x80' for c in s) 
#print test_ascii
s = ' '
try:
    s.decode('ascii')
except UnicodeDecodeError:
    print "s was not a ascii-encoded unicode string"
else:
    print "s may have been an ascii-encoded unicode string"
    '''
import numpy as np
import pylab as P
   
#
# now we create a cumulative histogram of the data
#
P.figure()

n, bins, patches = P.hist(x, 50, normed=1, histtype='step', cumulative=True)

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
P.ylim(0, 1.05)
