import urllib
import simplejson

#-----------------------------------------------------------------------------------------------------------------------------------#
class DataCruncher(object):
    """Handles scraping and cleaning of data"""

#-----------------------------------------------------------------------------------------------------------------------------------#
    def googleSearch(self, query):
        q = urllib.urlencode({'q': query})
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&rsz=8' %q
        search_results = urllib.urlopen(url)
        json = simplejson.loads(search_results.read())
        results = json['responseData']['results']
        lol=0