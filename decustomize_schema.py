# Convert a internal TIND CaltechDATA record into a  DataCite 4 standard schema json record to the customized internal
# schema used by TIND in CaltechDATA
import json
import argparse

def decustomize_schema(json_record):

    #Extract subjects to single string
    if "subjects" in json_record:
        subjects = json_record['subjects'].split(',')
        print(subjects)
        print("LFLF")
        array = []
        for s in subjects:
            array.append({'subject':s})
        json_record['subjects']=array

    #Extract identifier and label as DOI
    if "doi" in json_record:
        json_record['identifier'] = {'identifier':json_record['doi'],
                'identifierType':"DOI"}
        del json_record['doi']

    print(json_record)
    print("FUNFUN")
    exit()
    #Extract title
    if "titles" in json_record:
        titles = json_record['titles']
        for t in titles:
            if 'titleType' not in t:
                json_record['title']=t['title']

    #Change related identifier labels
    if "relatedIdentifiers" in json_record:
        for listing in json_record['relatedIdentifiers']:
            listing['relatedIdentifierRelation'] = listing.pop('relationType')
            listing['relatedIdentifierScheme'] = listing.pop('relatedIdentifierType')

    #change author formatting
    #We're only supporting ORCIDS, and losing all URIs
    if "creators" in json_record:
        authors = json_record['creators']
        newa = []
        for a in authors:
            new = {}
            if 'affiliations' in a:
                new['authorAffiliation'] = a['affiliations']
            new['authorName'] = a['creatorName']
            if 'nameIdentifiers' in a:
                for n in a['nameIdentifiers']:
                    if n['nameIdentifierScheme']=="ORCID":
                        new['nameIdentifiers']={"nameIdentifier":n["nameIdentifier"],
                            "NameIdentifierScheme": "ORCID"}
            newa.append(new)
        json_record['authors']=newa

    #strip creator URI
    if "contributors" in json_record:
        for c in json_record['contributors']:
            if 'nameIdentifiers' in c:
                for d in c['nameIdentifiers']:
                    if "schemeURI" in d:
                        d.pop("schemeURI")
            if 'familyName' in c:
                c.pop('familyName')
                c.pop('givenName')

    #format
    if "formats" in json_record:
        json_record['format']=json_record.pop('formats')

    #dates
    if "dates" in json_record:
        dates = json_record['dates']
        for d in dates:
            d['relevantDateValue']=d.pop('date')
            d['relevantDateType']=d.pop('dateType')
        json_record['relevantDates']=json_record.pop('dates')

    #license
    if 'rightsList' in json_record:
        licenses = json_record['rightsList']
        json_record['license']=licenses[0]['rights']
        #Only transfers first license
    
    #Funding
    if 'fundingReferences' in json_record:
        funding = json_record['fundingReferences']
        newf = []
        for f in funding:
            frec = {}
            if 'funderName' in f:
                frec['fundingName'] = f['funderName']
            #f['fundingName']=f.pop('funderName')
            if 'awardNumber' in f:
                frec['fundingAwardNumber']=f['awardNumber']['awardNumber']
            newf.append(frec)
        json_record['fundings']=newf
        #Some fields not preserved

    #Geo
    if 'geographicCoverage' in json_record:
        json_record['geographicCoverage'] = json_record.pop('geoLocations')

    #Publisher
    if "publisher" in json_record:
        publisher = {}
        publisher['publisherName'] = json_record['publisher']
        json_record['publishers'] = publisher

    #print(json.dumps(json_record))
    return json_record

if __name__ == "__main__":
    #Read in from file for demo purposes

    parser = argparse.ArgumentParser(description=\
                "customize_schema converts a DataCite 4 standard json record\
                to TIND customized internal schema in CaltechDATA")
    parser.add_argument('json_files', nargs='+', help='json file name')
    args = parser.parse_args()

    for jfile in args.json_files:
        infile = open(jfile,'r')
        data = json.load(infile)
        new = customize_schema(data)
        with open('formatted.json','w') as outfile:
            json.dump(new,outfile)
        #print(json.dumps(new))
