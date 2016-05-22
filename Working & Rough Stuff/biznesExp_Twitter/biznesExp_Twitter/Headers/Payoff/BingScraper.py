import urllib2
import re
import json

class BingScraper(object):
    """Contains machinery to scrape bing for search terms"""

    resultSet = None
    relevantResults = None
    tokens = None

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self):
        k = 0

#-----------------------------------------------------------------------------------------------------------------------------------#
    def bingSearch(self, query):
        self.tokens = list()
        self.relevantResults = dict()

        #keyBing = r'rh24GWrl3xpw/neQjctPCSOuHtRKjG2e0GmGkh30JR4'        # get Bing key from: https://datamarket.azure.com/account/keys
        keyBing = r'z2B/pKwbRAZQdcTiCVWybtZ3EWkVpaxTlGfL9norzjQ'        # get Bing key from: https://datamarket.azure.com/account/keys
        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
        #searchString = '%27Xbox+One%27'
        searchString = '%27' + '+'.join(query.split()) + '%27'
        top = 20
        offset = 0

        url = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?' + \
              'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

        request = urllib2.Request(url)
        request.add_header('Authorization', credentialBing)
        requestOpener = urllib2.build_opener()
        response = requestOpener.open(request) 

        results = json.load(response)

        self.resultSet = results['d']['results']
        self.populateRelevantResults()
        self.tokenizeRelevantResults()

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