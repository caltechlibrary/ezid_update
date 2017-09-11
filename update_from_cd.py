import os,json,csv
import requests
from datacite import DataCiteMDSClient, schema40
from EZID import EZIDClient
from decustomize_schema import decustomize_schema

def update_doi(doi,metadata,url):

    SERVER = "https://ezid.cdlib.org"
    ez=EZIDClient(SERVER,
    credentials={'username':os.environ['EZID_USER'],
    'password':os.environ['EZID_PWD']})
    sid = ez.login()

    assert schema40.validate(metadata)
    #Debugging if this fails
    #v = schema40.validator.validate(metadata)
    #errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
    #for error in errors:
    #        print(error.message)

    xml = schema40.tostring(metadata)

    #should verify that doi is in the form 10.xxx
    resp = ez.update('doi:'+doi,{'datacite':xml})
    print(resp)
    resp = ez.update('doi:'+doi,{'_target':url})

infile = open('dois.csv')
dois = csv.reader(infile)

for row in dois:

    api_url = "https://data.caltech.edu/api/record/"
    url = 'https://data.caltech.edu/records/'
    idv = row[1]
    
    r = requests.get(api_url+idv)
    metadata = r.json()['metadata']
    metadata = decustomize_schema(metadata)
    print(metadata)

    #update_doi(row[0],metadata,url+idv)
