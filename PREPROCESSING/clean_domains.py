'''
Created on Nov 3, 2014

@author: michal
'''
import trxFunctionsClass as trx
import generalMethods as gm

def create_clean_domains_file(src,dest):
    d = {}
    with open(src,"r") as f:      
        for line in f:
            d.setdefault(trx.getDomainFromRequestedSite(line.rstrip()),None)
 
    gm.saveDict(dest, d)
    return



main_dir = '/home/michal/SALSA_files/blackLists'

copy_full = '/'.join([main_dir,'copyrightDomains_full_domain'])
mal_full = '/'.join([main_dir,'malwareDomains_full_domain'])

copy = '/'.join([main_dir,'copyrightDomains'])
mal = '/'.join([main_dir,'malwareDomains'])

create_clean_domains_file(mal_full,mal)
create_clean_domains_file(copy_full,copy)

'''
IMPORTANT: you need to vi the file created and remove all ',' - :%s/,//
there was 1 empty domain- delete it
'''
    