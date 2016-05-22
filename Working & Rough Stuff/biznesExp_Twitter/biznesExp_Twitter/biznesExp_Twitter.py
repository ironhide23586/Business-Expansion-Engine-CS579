from Headers.TwitterCommunicator import *
from Headers.Payoff.PayoffCalculator import *
from Headers.Payoff.DataCruncher import *
from Headers.Payoff.GoogleScraper import *
from Headers.NetworkData import *


nData = NetworkData()
nData.loadFriendNetworkData('dump_friendNetworks_prev.txt')

tags = ['computer', 'electronics', 'laptop', 'phones', 'gadget']

pCalc = PayoffCalculator(nData.friendNetworks, tags)
pCalc.calculateAllPayoffs()
pCalc.dumpPayoffs()


#rel = pCalc.calculateRelevance('lindt', 'chocolate')

#print rel
#k=0

#dc = GoogleScraper()
#dc.googleSearch('hahaha')
#dc.tokenizeRelevantResults()

#tCom = TwitterCommunicator()

#nData = NetworkData(tCommObject=tCom)
#nData.loadFriendNetworkData('dump_friendNetworks_prev.txt')


#tCom = TwitterCommunicator(collectFriends=True)

#pCalc = DataCruncher(tCommObject=tCom)
#pCalc.collectFriendNetworkData()
#pCalc.dumpFriendNetworkData()

#keywords = raw_input("Please enter the keywords pertaining to the product you wish to publicize separated by a space: ")

#keywords = keywords.split(' ')

#lol