import pickle
import time

#-----------------------------------------------------------------------------------------------------------------------------------#
class NetworkData(object):
    """Handles scraping and cleaning of data"""

    twitterObject = None

    friendNetworks = dict()

#-----------------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, tCommObject=None):
        if tCommObject is not None:
            self.twitterObject = tCommObject

#-----------------------------------------------------------------------------------------------------------------------------------#
    def collectFriendNetworkData(self):
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
                    time.sleep(62)
            except:
                return
            
#-----------------------------------------------------------------------------------------------------------------------------------#
    def dumpFriendNetworkData(self, fileName='dump_friendNetworks.txt'):
        with open(fileName, 'wb') as fl:
            pickle.dump(self.friendNetworks, fl)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def loadFriendNetworkData(self, fileName='dump_friendNetworks.txt'):
        with open(fileName, 'rb') as fl:
            self.friendNetworks = pickle.load(fl)