from Headers.Payoff.GoogleScraper import *
from Headers.Payoff.BingScraper import *
import pickle
import numpy as np
import sys
import os

#-----------------------------------------------------------------------------------------------------------------------------------#
class PayoffCalculator(object):
    """Calculates payoff of a given object"""

    allNets = None 
    payOffs = None #Dictionary mapping each user to their respective payoffs
    tagSet = None #Contains the set of keywords input by user

    bSearch = None

    def __init__(self, nData, tagWords):
        """Class constructor which primes all variables for execution"""
        self.allNets = nData
        self.tagSet = tagWords
        self.payOffs = dict()
        self.bSearch = BingScraper()

    def calculateAllPayoffs(self):
        """Method to compute the payoffs of all friends of the user"""
        i = 1
        l = len(self.allNets.friendNetworks.keys())
        k=0
        for friend in self.allNets.friendNetworks.keys():
            try:
                print 'Processing entry', friend, '(', i, '/', l, ')'
                self.payOffs[friend] = self.calculatePayoff(friend)
                print friend, ', Payoff = ', self.payOffs[friend]

                fname = 'payoffupto' + str(k)
                with open(fname, 'wb') as fl: #Dumps each payoff computed as it is time consuming
                    pickle.dump(self.payOffs, fl)
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

            k = k + 1
            i = i + 1

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
        """Calculates the payoff for a person pertaining to the input set of keywords.
        Args:
        Username of person for whom the payoff is to be calculated.
        Returns:
        Value(s) from 0 to 1 which is the payoff of the given product for the user."""
        
        totalScore = 0.
        count = 0
        nGram = 5

        chosenFriends = [k['name'] for k in self.allNets.friendNetworks[friend].get_iterator() if (k['verified'] == True or k['followers_count'] > 200)]
        netSize = len(chosenFriends)

        if netSize == 0:
            return 0.

        tagSize = len(self.tagSet)

        tagCounts = np.zeros((netSize, tagSize))

        rms = np.zeros(tagSize)

        row = 0
        for k in chosenFriends: #k is a person/page in friend's network
            try:
                print 'Calculating payoff potential for', k, '(', row+1, '/', netSize, ')'
                tmp = self.calculateIndividualPayoff(k, self.tagSet, nGram)
                tagCounts[row, :] = tmp
                lol=0
                #row = row + 1
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                #input('')
            row = row + 1

        #Normalizing matrix
        for i in range(tagSize):
            rms[i] = np.linalg.norm(tagCounts[:, i])
            if rms[i] == 0:
                rms[i] = 1

        normalTagCounts = tagCounts / rms
        p=normalTagCounts[~np.all(normalTagCounts == 0, axis=1)]
        score = np.mean(p)
        return score
        
#-----------------------------------------------------------------------------------------------------------------------------------#
    def calculateIndividualPayoff(self, product, tags, nGram):
        """ Calculates the affinities between a given page name and the input keywords
        Args:
          product .... Name of a page (which a user follows)
          tags .... Set of keywords entered by user
          nGram .... The maximum distance within which, the product name and the keyword must occur in the token list to be considered.
        Returns:
          cnts .... The number of occurences in the token list returned by the bing search which contain the page name and the keyword within
          a given range defined by nGram
        """
        cnts = np.zeros(len(tags))
        col = 0
        for tag in tags:
            self.bSearch.bingSearch(product + ' and ' + tag)
            i = 0
            tmp = 0
            for token in self.bSearch.tokens:
                chunk = self.bSearch.tokens[i:i+nGram]
                if product.lower().strip() in chunk and tag.lower().strip() in chunk:
                    tmp = tmp + 1
                i = i + 1
            cnts[col] = tmp
            col = col + 1
        return cnts
