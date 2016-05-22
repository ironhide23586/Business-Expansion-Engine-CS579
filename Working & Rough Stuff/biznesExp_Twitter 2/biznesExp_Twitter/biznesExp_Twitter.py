from Headers.TwitterCommunicator import *
from Headers.Payoff.PayoffCalculator import *
from Headers.Payoff.DataCruncher import *
from Headers.Payoff.GoogleScraper import *
from Headers.NetworkData import *


nData = NetworkData()
nData.loadFriendNetworkData('dump_friendNetworks_prev.txt')

tags = ['computer', 'electronics', 'laptop', 'phones', 'gadget']

pCalc = PayoffCalculator(nData, tags)
pCalc.calculateAllPayoffs()
#pCalc.calculateIndividualPayoff('doritos', tags, 5)
pCalc.dumpPayoffs()

#pCalc.loadPayoffs()
#lol=0