from collections import Counter
import ConfigParser
import sys
import time
from TwitterAPI import TwitterAPI

#-----------------------------------------------------------------------------------------------------------------------------------#
class TwitterCommunicator(object):
    """Handles all communications being made with Twitter."""

    twitterObject = None
    my_friends_all = None
    my_friends_filtered = list()
#-----------------------------------------------------------------------------------------------------------------------------------#
    """Twittter App specific details needed to make a connection"""
    __default_consumer_key = '6SulyluGKFESIaRLUddaRknWQ'
    __default_consumer_secret = 'SMHXxwCqxyW1FX4XWSX6qHQPBdY2hgw6qkyP0vWJq1sVWtIKox'
    __default_access_token = '3236799931-xfe9VLcyFAVtJOxyRpJWUMv0z0zrrXpYt6tA0gs'
    __default_access_token_secret = '7Z3a30oalopdayuM7eGHxf7paK9mgLQxHyzOiyy8ASnvV'

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, uname='ironhide23586', con_file=None, collectFriends=False):
        """Initializes class twitter object named 'twitterObject' & stores friend list of input user in 
        class variable 'my_friends_all'"""
        if con_file is not None:
            self.twitterObject = self.__get_twitter(con_file)
        else:
            self.twitterObject = self.__get_twitter()

        if collectFriends is True:
            self.my_friends_all = self.get_friends(uname)
            for f in self.my_friends_all.get_iterator():
                 if f['verified']==False:
                     self.my_friends_filtered.append(f)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __get_twitter(self, config_file=None):
        """ Read the config_file and construct an instance of TwitterAPI.
        Args:
          config_file ... A config file in ConfigParser format with Twitter credentials
        Returns:
          An instance of TwitterAPI.
        """

        if config_file is not None:
            config = ConfigParser.ConfigParser()
            config.read(config_file)
            twitter = TwitterAPI(
                           config.get('twitter', 'consumer_key'),
                           config.get('twitter', 'consumer_secret'),
                           config.get('twitter', 'access_token'),
                           config.get('twitter', 'access_token_secret'))
        else:
            twitter = TwitterAPI(
                           self.__default_consumer_key,
                           self.__default_consumer_secret,
                           self.__default_access_token,
                           self.__default_access_token_secret)
            
        return twitter

#-----------------------------------------------------------------------------------------------------------------------------------#
    def robust_request(self, twitter, resource, params, max_tries=5):
        """ If a Twitter request fails, sleep for 15 minutes.
        Do this at most max_tries times before quitting.
        Args:
          twitter .... A TwitterAPI object.
          resource ... A resource string to request.
          params ..... A parameter dictionary for the request.
          max_tries .. The maximum number of tries to attempt.
        Returns:
          A TwitterResponse object, or None if failed.
        """
        for i in range(max_tries):
            request = twitter.request(resource, params)
            if request.status_code == 200:
                return request
            else:
                print >> sys.stderr, 'Got error:', request.text, '\nsleeping for 15 minutes.'
                sys.stderr.flush()
                time.sleep(61 * 15)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def get_friends(self, screen_name):
        """ Return a list of the users that this person follows on Twitter, up to 200.
        See https://dev.twitter.com/rest/reference/get/friends/list 
        Note, because of rate limits, it's best to test this method for one candidate before trying
        on all candidates.
    
        Args:
            screen_name: a string of a Twitter screen name
        Returns:
            A list of strings, one per friend.
        Note: Many users follow more than 200 accounts; we will limit ourselves to
        the first 200 accounts returned.
        """
        # TODO
        return self.robust_request(self.twitterObject, 'friends/list', {'screen_name': screen_name, 'count': 200})

