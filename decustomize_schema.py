# Convert a internal TIND CaltechDATA record into a  DataCite 4 standard schema json record
import json
import argparse

def decustomize_schema(json_record):

    #Extract subjects to single string
    if "subjects" in json_record:
        subjects = json_record['subjects'].split(',')
        array = []
        for s in subjects:
            array.append({'subject':s})
        json_record['subjects']=array

    #Extract identifier and label as DOI
    if "doi" in json_record:
        json_record['identifier'] = {'identifier':json_record['doi'],
                'identifierType':"DOI"}
        del json_record['doi']

    #Extract title
    if "title" in json_record:
        json_record['titles'] = [{"title":json_record['title']}]
        del json_record['title']

    #Change related identifier labels
    if "relatedIdentifiers" in json_record:
        for listing in json_record['relatedIdentifiers']:
            listing['relationType'] = listing.pop('relatedIdentifierRelation') 
            listing['relatedIdentifierType'] = listing.pop('relatedIdentifierScheme')

    #change author formatting
    #Could do better with multiple affiliations
    if "authors" in json_record:
        authors = json_record['authors']
        newa = []
        for a in authors:
            new = {}
            if 'authorAffiliation' in a:
                new['affiliations'] = [a['authorAffiliation']]
            new['creatorName'] = a['authorName']
            newa.append(new)
        json_record['creators']=newa
        del json_record['authors']

    #contributors
    if "contributors" in json_record:
        for c in json_record['contributors']:
            if 'contributorAffiliation' in c:
                c['affiliations'] = [c.pop('contributorAffiliation')]
            if 'contributorIdentifiers' in c:
                for d in c['contributorIdentifiers']:
                    d['nameIdentifier'] = d.pop('contributorIdentifier')
                    d['nameIdentifierScheme'] = d.pop('contributorIdentifierScheme')
                c['nameIdentifiers'] = c.pop('contributorIdentifiers')
            if 'contributorEmail' in c:
                del c['contributorEmail']
    #format
    if "format" in json_record:
        json_record['formats']=[json_record.pop('format')]

    #dates
    if "relevantDates" in json_record:
        dates = json_record['relevantDates']
        for d in dates:
            d['dates']=d.pop('relevantDateValue')
            d['dateType']=d.pop('relevantdateType')
        json_record['dates']=json_record.pop('relevantDates')

    #set publicationYear
    year = json_record['publicationDate'].split('-')[0]
    json_record['publicationYear'] = year
    del json_record['publicationDate']

    #license - no url available
    if 'license' in json_record:
        json_record['rightsList']=[{"rights":json_record.pop('license')}]
    
    #Funding
    if 'fundings' in json_record:
        funding = json_record['fundings']
        newf = []
        for f in funding:
            frec = {}
            if 'fundingName' in f:
                frec['funderName'] = f['fundingName']
            #f['fundingName']=f.pop('funderName')
            if 'fundingAwardNumber' in f:
                frec['awardNumber']=f['fundingAwardNumber']
            newf.append(frec)
        json_record['fundings']=newf

    #Geo
    if 'geoLocations' in json_record:
        json_record['geoLocations'] = json_record.pop('geographicCoverage')

    #Publisher
    if "publishers" in json_record:
        json_record['publisher'] = json_record['publishers']['publisherName']
        del json_record['publishers']

    #description
    if "descriptions" in json_record:
        for d in json_record["descriptions"]:
            d["description"] = d.pop("descriptionValue")

    others = ['files', 'owners', 'pid_value', 'control_number', '_oai',
            '_form_uuid', 'electronic_location_and_access', 'access_right']
    for v in others:
        del json_record[v]

    #print(json.dumps(json_record))
    return json_record

if __name__ == "__main__":
    #Read in from file for demo purposes

    parser = argparse.ArgumentParser(description=\
                "decustomize_schema converts a internal TIND CaltechDATA record\
       into a  DataCite 4 standard schema json record")
    parser.add_argument('json_files', nargs='+', help='json file name')
    args = parser.parse_args()

    for jfile in args.json_files:
        infile = open(jfile,'r')
        data = json.load(infile)
        new = customize_schema(data)
        with open('formatted.json','w') as outfile:
            json.dump(new,outfile)
        #print(json.dumps(new))
