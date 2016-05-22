from Headers.Payoff.GoogleScraper import *
from Headers.Payoff.BingScraper import *
import pickle
import numpy as np

try:
    from nltk.tag import pos_tag
except :
    k = 0

#-----------------------------------------------------------------------------------------------------------------------------------#
class PayoffCalculator(object):
    """Calculates payoff of a given object
    Args:
        Username(s) of person for whom the payoff is to be calculated.
        Keywords Pertaining to the product
    Returns:
        Value(s) from 0 to 1 which is the payoff of the given product for the user."""


    allNets = None
    payOffs = None
    tagSet = None

    def __init__(self, nData, tagWords):
        self.allNets = nData
        self.tagSet = tagWords
        self.payOffs = dict()

    def calculateAllPayoffs(self):
        i = 1
        l = len(self.allNets.friendNetworks.keys())
        for friend in self.allNets.friendNetworks.keys():
            #try:
            #    print 'Processing entry', friend, '(', i, '/', l, ')'
            #    self.payOffs[friend] = self.calculatePayoff(friend)
            #    print friend, ', Payoff = ', self.payOffs[friend]
            #except:
            #    return
            print 'Processing entry', friend, '(', i, '/', l, ')'
            self.payOffs[friend] = self.calculatePayoff(friend)
            print friend, ', Payoff = ', self.payOffs[friend]

#-----------------------------------------------------------------------------------------------------------------------------------#
    def dumpPayoffs(self, fileName='dump_payoffs.txt'):
        with open(fileName, 'wb') as fl:
            pickle.dump(self.payOffs, fl)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def loadPayoffs(self, fileName='dump_payoffs.txt'):
        with open(fileName, 'rb') as fl:
            self.payOffs = pickle.load(fl)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def calculatePayoff(self, friend):
        """Returns the payoff for the input user"""
        totalScore = 0.
        count = 0
        nGram = 5

        chosenFriends = [k['name'] for k in self.allNets.friendNetworks[friend].get_iterator() if (k['verified'] == True or k['followers_count'] > 200)]

        #netSize = len(list(self.friendNetworks[friend].get_iterator()))
        netSize = len(chosenFriends)
        tagSize = len(self.tagSet)

        tagCounts = np.zeros((netSize, tagSize))

        rms = np.zeros(tagSize)

        row = 0
        for k in chosenFriends: #k is a person/page in friend's network
            print 'Calculating payoff potential for', k, '(', row+1, '/', netSize, ')'
            tagCounts[row, :] = self.calculateIndividualPayoff(k, self.tagSet, nGram)
            row = row + 1

        #Normalizing matrix
        for i in range(tagSize):
            rms[i] = np.linalg.norm(tagCounts[:, i])
            if rms[i] == 0:
                rms[i] = 1

        normalTagCounts = tagCounts / rms

        score = np.mean(normalTagCounts)
        return score

#-----------------------------------------------------------------------------------------------------------------------------------#
    def calculateIndividualPayoff(self, product, tags, nGram):
        bSearch = BingScraper()
        cnts = np.zeros(len(tags))
        col = 0
        for tag in tags:
            bSearch.bingSearch(product + ' and ' + tag)
            i = 0
            tmp = 0
            for token in bSearch.tokens:
                chunk = bSearch.tokens[i:i+nGram]
                #print chunk
                if product in chunk and tag in chunk:
                    tmp = tmp + 1
                    #print 'YAY'
                i = i + 1
            #print tmp
            cnts[col] = tmp
            col = col + 1
        return cnts