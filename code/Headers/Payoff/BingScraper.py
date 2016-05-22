import urllib2
import re
import json
import os
import sys

class BingScraper(object):
    """Contains machinery to scrape Bing for search terms"""

    resultSet = None #Raw set of unfiltered, unparsed results returned from initial Bing Search
    relevantResults = None #Contains the title and description extracted from the data in the resultSet
    tokens = None #Central class object containing the list of tokens from which extraneous words have been filtered out

    keyTable = None #Table containing list of Bing Search API keys to be used for searching
    currentWorkingKey = 0 #Index of current search API key being used to search

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self):
        """Class Constructor which loads the list of available API search keys and primes the class for search command execution"""
        try:
            f = open('searchKeys.txt')
            keys = f.readlines()
            #self.keyTable = [key[:-1] for key in keys if key[-1]=='\n']
            self.keyTable = list()
            for key in keys:
                if key[-1]=='\n':
                    self.keyTable.append(key[:-1])
                else:
                    self.keyTable.append(key)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def bingSearch(self, query):
        """ Performs a programmatic Bing Search
        Args:
          query .... String to be searched
        Returns:
          Nothing, just populates the class variables containing the search result tokens.
        """
        query = re.sub('[^a-zA-Z0-9-_*.]', ' ', query) #Filters input query for only alphanumeric characters
        self.tokens = list()
        self.relevantResults = dict()
        self.resultSet = None

        keyBing = self.keyTable[self.currentWorkingKey] #Gets working serach API key

        credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
        searchString = '%27' + '+'.join(query.split()) + '%27'
        top = 20
        offset = 0

        url = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?' + \
              'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

        request = urllib2.Request(url)
        request.add_header('Authorization', credentialBing)
        requestOpener = urllib2.build_opener()
        
        try:
            response = requestOpener.open(request) 
            results = json.load(response)
            self.resultSet = results['d']['results']
            self.populateRelevantResults()
            self.tokenizeRelevantResults()
        except Exception as e:
            #Switches search API key to new working key in case of a failed search
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print 'PREVIOUS working key index =', self.currentWorkingKey
            #input('')

            self.currentWorkingKey = self.currentWorkingKey + 1
            print 'UPDATED working key index =', self.currentWorkingKey
            if self.currentWorkingKey < len(self.keyTable):
                self.bingSearch(query)
            else:
                print 'Ran out of search transactions. Add more search keys. :('

#-----------------------------------------------------------------------------------------------------------------------------------#
    def populateRelevantResults(self):
        """Extracts the title and description fields from the raw search results"""
        for r in self.resultSet:
            self.relevantResults[r['Title']]=r['Description']

 #-----------------------------------------------------------------------------------------------------------------------------------#
    def getTokens(self, text):
        """Tokenizes input text and filters out extraneous words."""
        text = re.sub(r"[\W]", ' ', unicode(text.lower()))
        text = re.sub('\s+(a|an|and|the|of|on|is|was|were|from|to|for|in|while|at|there|with)(\s+)', ' ', text)
        text = re.sub('\s+(\D)(\s+)', ' ', text)
        self.tokens += text.split()

#-----------------------------------------------------------------------------------------------------------------------------------#
    def tokenizeRelevantResults(self):
        """Populates the class variable containing list of tokens after filtering out irrelevant and redundant words."""
        for k in self.relevantResults.iterkeys():
            self.getTokens(self.relevantResults[k])
            self.getTokens(k)
