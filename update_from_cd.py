import os,json,csv
import requests
from datacite import DataCiteMDSClient, schema40
from EZID import EZIDClient
from decustomize_schema import decustomize_schema
from update_doi import update_doi

infile = open('dois.csv')
dois = csv.reader(infile)

for row in dois:

    api_url = "https://data.caltech.edu/api/record/"
    url = 'https://data.caltech.edu/records/'
    idv = row[1]
    
    r = requests.get(api_url+idv)
    metadata = r.json()['metadata']
    metadata = decustomize_schema(metadata)

    update_doi(row[0],metadata,url+idv)
