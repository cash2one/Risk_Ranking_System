#!/usr/local/anaconda/bin/python2.7
'''
Created on Jul 28, 2014

@author: michal
'''

import linesClass 
import csv

'''
def DEBUG_domains_as_curdomain():
    global l
    Label = linesClass.lbl
    d = {}
    for line in l.lines:
        d[line[Label.domain]] = 0
    
    for k in d:
        print k
        
    return'''
    
debug_file = '/home/michal/SALSA_files/tmp/DEBUG_output.csv'
    
def check_if_prev_diff_from_curr_domain(lines):
    lbl = linesClass.lbl
    num_of_lines_with_prev_domain = 0
    num_of_diff_prevDomain_from_curDomain = 0
    with open(debug_file, "wb") as f:
        w = csv.writer(f, delimiter='\t')
        for line in lines:
            if line[lbl.prevDomain]:
                num_of_lines_with_prev_domain += 1
                if line[lbl.prevDomain] != line[lbl.domain]:
                    num_of_diff_prevDomain_from_curDomain += 1
                    w.writerow([ 'line idx:' , str(lines.index(line)) , \
                                'prevDomain:' , line[lbl.prevDomain] , \
                                'curDomain:' , line[lbl.domain]])
        w.writerow([ '----------------------------' ])
        w.writerow([ 'num of lines:' , str(len(lines)) ])
        w.writerow([ 'num of lines with prevDomain:' , str(num_of_lines_with_prev_domain) ])
        w.writerow([ 'num of lines with diff prevDomain than curDomain:' , str(num_of_diff_prevDomain_from_curDomain) ])
    return



    

    