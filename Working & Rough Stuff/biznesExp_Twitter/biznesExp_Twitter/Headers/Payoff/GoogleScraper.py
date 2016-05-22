import urllib
import simplejson
import re

#-----------------------------------------------------------------------------------------------------------------------------------#
class GoogleScraper(object):
    """Contains machinery to scrape google for search terms"""

    resultSet = None
    relevantResults = None
    tokens = None

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self):
        k = 0

#-----------------------------------------------------------------------------------------------------------------------------------#
    def googleSearch(self, query):
        self.tokens = list()
        self.relevantResults = dict()
        q = urllib.urlencode({'q': query})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&rsz=8' %q
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        self.resultSet = json['responseData']['results']
        self.populateRelevantResults()
        self.tokenizeRelevantResults()

#-----------------------------------------------------------------------------------------------------------------------------------#
    def populateRelevantResults(self):
        for r in self.resultSet:
            self.relevantResults[r['titleNoFormatting']]=r['content']

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
