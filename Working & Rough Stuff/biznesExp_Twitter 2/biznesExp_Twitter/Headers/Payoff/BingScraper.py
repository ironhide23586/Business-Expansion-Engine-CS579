import urllib2
import re
import json

class BingScraper(object):
    """Contains machinery to scrape Bing for search terms"""

    resultSet = None
    relevantResults = None
    tokens = None

    keyTable = None
    currentWorkingKey = 0

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self):
        f = open('searchKeys.txt')
        keys = f.readlines()
        self.keyTable = [key[:-1] for key in keys]

#-----------------------------------------------------------------------------------------------------------------------------------#
    def bingSearch(self, query):
        query = query.encode('ascii','ignore')
        self.tokens = list()
        self.relevantResults = dict()

        #keyBing = r'rh24GWrl3xpw/neQjctPCSOuHtRKjG2e0GmGkh30JR4'        # get Bing key from: https://datamarket.azure.com/account/keys
        #keyBing = r'z2B/pKwbRAZQdcTiCVWybtZ3EWkVpaxTlGfL9norzjQ'        # get Bing key from: https://datamarket.azure.com/account/keys
        #keyBing = r'ndMcDioomqhyvzi0rMUPbo+ub5Td7+kQC8J3Mq0es+I'
        #keyBing = r'79+dEwn+GUd/oM40Y5vQPPg8qM71S+VbuEPIoM1Awjw'
        #keyBing = r'+IarkIejrSnfdzQXNU0x3hp9fBhFNRcqDyRKf2oa8bk'
        #keyBing = r'vOZW8/mYRPTSg6xhGHIEVQau7mQmBMtpT1rmarNEkCM'
        #keyBing = r'iA3F9JQQ+Wu+2dWhQSA4qdKct0RKxgSgaw/aBuvNoho'
        keyBing = self.keyTable[self.currentWorkingKey]

        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
        searchString = '%27' + '+'.join(query.split()) + '%27'
        top = 20
        offset = 0

        url = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?' + \
              'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

        request = urllib2.Request(url)
        request.add_header('Authorization', credentialBing)
        requestOpener = urllib2.build_opener()

        #response = requestOpener.open(request) 
        #results = json.load(response)
        
        try:
            response = requestOpener.open(request) 
            results = json.load(response)
            self.resultSet = results['d']['results']
            self.populateRelevantResults()
            self.tokenizeRelevantResults()
        except:
            self.currentWorkingKey = self.currentWorkingKey + 1
            self.bingSearch(query)

        #self.resultSet = results['d']['results']
        #self.populateRelevantResults()
        #self.tokenizeRelevantResults()

#-----------------------------------------------------------------------------------------------------------------------------------#
    def populateRelevantResults(self):
        for r in self.resultSet:
            self.relevantResults[r['Title']]=r['Description']

 #-----------------------------------------------------------------------------------------------------------------------------------#
    def getTokens(self, text):
        text = re.sub(r"[\W]", ' ', unicode(text.lower()))
        text = re.sub('\s+(a|an|and|the|of|on|is|was|were|from|to|for|in|while|at|there|with)(\s+)', ' ', text)
        text = re.sub('\s+(\D)(\s+)', ' ', text)
        self.tokens += text.split()

#-----------------------------------------------------------------------------------------------------------------------------------#
    def tokenizeRelevantResults(self):
        for k in self.relevantResults.iterkeys():
            self.getTokens(self.relevantResults[k])
            self.getTokens(k)