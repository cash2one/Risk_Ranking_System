a=['b',0]
print a[0],hex(id([0]))
a[0]=['a']
print [0],hex(id([0]))
