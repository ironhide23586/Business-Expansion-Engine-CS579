from Headers.Payoff.GoogleScraper import *
from Headers.Payoff.BingScraper import *
import pickle

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


    friendNetworks = None
    payOffs = None
    tagSet = None

    def __init__(self, nData, tagWords):
        self.friendNetworks = nData
        self.tagSet = tagWords
        self.payOffs = dict()

    def calculateAllPayoffs(self):
        for friend in self.friendNetworks.keys():
            print 'Calculating payoff for', friend, '.....'
            self.payOffs[friend] = self.calculatePayoff(friend)
            print friend, ', Payoff = ', self.payOffs[friend]
            lol=0

#-----------------------------------------------------------------------------------------------------------------------------------#
    def dumpPayoffs(self, fileName='dump_payoffs.txt'):
        with open(fileName, 'wb') as fl:
            pickle.dump(self.payOffs, fl)

#-----------------------------------------------------------------------------------------------------------------------------------#
    def calculatePayoff(self, friend):
        """Returns the payoff for the input user"""
        totalScore = 0.
        count = 0
        for wTag in self.tagSet:
            for k in self.friendNetworks[friend].get_iterator():
                if k['verified'] == True or k['followers_count'] > 200:
                    try:
                        wFollow = k['name'].strip()
                        #print 'Processing words - ', wTag, '&', wFollow
                        relevance = self.calculateRelevance(wTag, wFollow)
                        #print friend, 'Relevance between', wTag, '&', wFollow, '=', relevance
                        if relevance > .17:
                            totalScore = totalScore + 1.
                            #print 'WORD IS RELEVANT'
                        #else:
                            #print 'WORD IS IRRELEVANT'
                        #print 'Total Score = ', totalScore
                    except:
                        tmp=0
                    count = count + 1.
        #print 'COUNT = ', count
        score = totalScore/float(count)
        return score

#-----------------------------------------------------------------------------------------------------------------------------------#
    def calculateRelevance(self, w0, w1):
        """Calculates the degree of relevance that w0 has with w1"""

        #g0 = BingScraper()
        #g0.bingSearch(w0)
        #g1 = BingScraper()
        #g1.bingSearch(w1)

        #g0_tags = pos_tag(g0.tokens)
        #g1_tags = pos_tag(g1.tokens)

        #s0_exclude = set([word for word, pos in g0_tags if pos == 'JJS' or pos == 'JJR' or pos == 'RB' or pos == 'TO' or pos == 'CD' or pos == 'IN' or pos == 'EX' or pos == 'PRP' or pos == 'PRP$' or pos == 'DT'])
        #s1_exclude = set([word for word, pos in g1_tags if pos == 'JJS' or pos == 'JJR' or pos == 'RB' or pos == 'TO' or pos == 'CD' or pos == 'IN' or pos == 'EX' or pos == 'PRP' or pos == 'PRP$' or pos == 'DT'])

        targPos0 = pos_tag([w0])[0][1]
        targPos1 = pos_tag([w1])[0][1]

        score = 0
        if targPos0 == targPos1:
            score = 1


        #s0 = set([word for word, pos in g0_tags if pos == targPos0])
        #s1 = set([word for word, pos in g1_tags if pos == targPos1])

        #s0 = set(g0.tokens) - s0_exclude
        #s1 = set(g1.tokens) - s1_exclude

        #s0 = set(g0.tokens)
        #s1 = set(g1.tokens)
        #cross = len(s0 & s1)
        ##print 'cross = ', cross
        ##print 's0 = ', len(s0), 's1 = ', len(s1), 's0|s1 = ', len(s0 | s1) 
        #try:
        #    score = (cross / float(len(s0)) + cross / float(len(s1))) / float(2)
        #except:
        #    score = 0.
        #return (cross / float(all))
        return score