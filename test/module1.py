import graphlab
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