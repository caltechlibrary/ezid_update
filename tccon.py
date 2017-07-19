import os
from EZID import EZIDClient

SERVER = "https://ezid.cdlib.org"
ez=EZIDClient(SERVER,
credentials={'username':os.environ['EZID_USER'],
'password':os.environ['EZID_PWD']})
sid = ez.login()

inputf = "doi_list.txt"
infile = open(inputf,'r')
doi = infile.readline()
head = "ftp://tccon.ornl.gov/2014Public/"
revised_list = []
zero_list = []
zero_doi = []
while doi != '':
    split = doi.split('/')
    dsplit = split[1].split('.')
    if dsplit[3] =='R1':
        resp = ez.update(doi,{'_target':head+dsplit[2].lower()})
        print(resp)
        print(doi+"<<>>"+ head+dsplit[2].lower())
        revised_list.append(dsplit[2].lower())
    elif dsplit[3] =='R0':
        zero_list.append(dsplit[2].lower())
        zero_doi.append(doi)
    else:
        print("!!! No match to "+ doi)
    doi = infile.readline()

#We need to determine if files are at /site or /site/R0_archive
for sn in range(len(zero_list)):
    if zero_list[sn] in revised_list:
        resp = ez.update(zero_doi[sn],{'_target':head+zero_list[sn]+'/R0_archive/'})
        print(resp)
        print(zero_doi[sn]+"<<>>"+head+zero_list[sn]+'/R0_archive/')
    else:
        resp = ez.update(zero_doi[sn],{'_target':head+zero_list[sn]})
        print(resp)
        print(zero_doi[sn]+"<<>>"+head+zero_list[sn])

        
