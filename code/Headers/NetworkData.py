import pickle
import time

#-----------------------------------------------------------------------------------------------------------------------------------#
class NetworkData(object):
    """Handles scraping and cleaning of data"""

    twitterObject = None #Central twitter object of the class

    friendNetworks = dict() #Dictionary mapping each friend of the user to his/her friends/pages he/she follows.

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, tCommObject=None):
        """Class constructor which initializes the central twitter object of the class with input twitter object if provided"""
        if tCommObject is not None:
            self.twitterObject = tCommObject

#-----------------------------------------------------------------------------------------------------------------------------------#
    def collectFriendNetworkData(self):
        """Collects the friends/pages followed by the friends of user"""
        i = 1
        k = False
        l = len(self.twitterObject.my_friends_filtered)
        if l > 14:
            k = True 
        for friend in self.twitterObject.my_friends_filtered:
            try:
                sName = friend['screen_name']
                self.friendNetworks[sName] = self.twitterObject.get_friends(sName)
                print 'Collecting data for friend no.', i, 'out of', l, 'total legit friends lolllll :P'
                i = i + 1
                if k is True:
                    time.sleep(62) #Sleep for 62 seconds after each API request due to API request rate limitations.
            except:
                return
            
#-----------------------------------------------------------------------------------------------------------------------------------#
    def dumpFriendNetworkData(self, fileName='dump_friendNetworks.txt'):
        """Dumps dictionary mapping user's friends to their friends/pages to serialized file on hard disk using pickle."""
        with open(fileName, 'wb') as fl:
            pickle.dump(self.friendNetworks, fl)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def loadFriendNetworkData(self, fileName='dump_friendNetworks.txt'):
        """Loads dictionary mapping user's friends to their friends/pages from serialized file on hard disk using pickle."""
        with open(fileName, 'rb') as fl:
            self.friendNetworks = pickle.load(fl)
