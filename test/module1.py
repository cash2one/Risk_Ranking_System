#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 20, 2014

@author: michal
'''
#import module2

# global G2
'''

G2=module2.G

print G2
print 'jkl'
G2+=[5]

print G2; print module2.G

M2=module2.M
mem2=M2.member2
print M2.member1;print M2.member2

mem2+=[888]
print M2.member2;print mem2; print module2.M.member2




print '--------------------------------------------------'
def func1():
    global var; var={'a1':1,'a2':2}
    return

def func2():
    global var; var['a3']=3
    return
#print var; 
module2.func1(); print var; module2.func2(); print var; var['a4']=4; print var'''



'''from numpy import cumsum
from operator import itemgetter

d={'dan':0.5, 'mike':0.2, 'john':0.3}

#unzip keys from values in a sorted order
keys, values = zip(*sorted(d.items(), key=itemgetter(1)))
total = sum(values)

# calculate cumsum and zip with keys into new dict
#d_cump = dict(zip(keys, (round(float(subtotal)/total,3) for subtotal in cumsum(values))))
cum_list = zip(keys, (round(float(subtotal)/total,3) for subtotal in cumsum(values)))
print cum_list
buckets = {}

num_of_buckets = 2
cur_bucket = num_of_buckets
bucket_capacity = 1.0/num_of_buckets
bucket_threshold = bucket_capacity
buckets.setdefault(cur_bucket,{}).setdefault('elements',[])    #init for the first (last actually) bucket

for k,v in cum_list:
    if v < bucket_threshold:
        buckets[cur_bucket]['elements'].append(k)
    else:   # new bucket
        buckets[cur_bucket]['max_val'] = d[buckets[cur_bucket]['elements'][-1]]    # update max value of bucket before opening a new bucket
        cur_bucket -= 1
        bucket_threshold += bucket_capacity
        buckets.setdefault(cur_bucket,{}).setdefault('elements',[])    #init new bucket
        buckets[cur_bucket]['elements'].append(k)
        
        

buckets[cur_bucket]['max_val'] = d[buckets[cur_bucket]['elements'][-1]]    # update max value of last bucket
'''

'''
from numpy import cumsum
from operator import itemgetter

d={'dan':0.5, 'mike':0.2, 'john':0.3}
num_of_buckets = 2

#unzip keys from values in a sorted order
sorted_d = sorted(d.items(), key=itemgetter(1))

buckets = {}

cur_bucket = num_of_buckets-1
bucket_capacity = 1.0/num_of_buckets
bucket_threshold = bucket_capacity
buckets.setdefault(cur_bucket,{}).setdefault('elements',[])    #init for the first (lowest scores) bucket
cum_sum = 0

for k,v in sorted_d:
    if cur_bucket:
        cum_sum += v
        if cum_sum < bucket_threshold:
            buckets[cur_bucket]['elements'].append(k)
        else:   # new bucket
            cur_bucket -= 1
            bucket_threshold += bucket_capacity
            buckets.setdefault(cur_bucket,{}).setdefault('elements',[k])    #init new bucket
    else:
        buckets[cur_bucket]['elements'].append(k)
    
# update buckets with general info:
for b in buckets:
    buckets[b]['min_val'] = d[buckets[b]['elements'][0]]    # update min value
    buckets[b]['max_val'] = d[buckets[b]['elements'][-1]]    # update max value
    buckets[b]['num_of_elements'] = len(buckets[b]['elements'])

print buckets
'''

'''alg1 = 'pagerank'
alg2 = 'inverse_pagerank'
alg3 = 'not_pr_at_all'

if 'pagerank' in alg1:
    print alg1
if 'pagerank' in alg2:
    print alg2
if 'pagerank' in alg3:
    print alg3
'''
def func():
    import module2
    print '\t---module1---'
    M = module2.M
    mem2 = module2.M.member2
    M.set_mem2()
    print M.member2; print mem2
    M.clear()
    print '====';print M.member2; print mem2
    M.set_mem2()
    print '====';print M.member2; print mem2
    return
        
    

''''a = 0.0
b = 0.000000000000000000001
c = 0
if a == 0: print 'a 0'
if b == 0: print 'b 0'
if c == 0: print 'c 0'
if a == 0.: print 'a 0.'
if a == 0.: print 'b 0.'
if a == 0.: print 'c 0.'

spc = ' '
if spc != ' ': print 'space' '''

listVar = []
listVar.append('a')
listVar.append('').append('b')
#listVar.append('b')
print listVar[0] + ',' +str(listVar[1])+','+listVar[2] 
if listVar[0]:
    print 'listVar[0] entered if'
if listVar[1]:
    print 'listVar[1] entered if'



    
    

