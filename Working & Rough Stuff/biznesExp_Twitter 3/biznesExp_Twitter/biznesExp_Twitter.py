from Headers.TwitterCommunicator import *
from Headers.Payoff.PayoffCalculator import *
from Headers.Payoff.DataCruncher import *
from Headers.Payoff.GoogleScraper import *
from Headers.NetworkData import *


nData = NetworkData()
nData.loadFriendNetworkData('dump_friendNetworks_prev.txt')

#del nData.friendNetworks['Deepanshu2014Dt']

#tags = ['computer', 'electronics', 'laptop', 'phones', 'gadget']

tags = ['celebrity', 'famous', 'party']

pCalc = PayoffCalculator(nData, tags)

#print pCalc.calculatePayoff('sowmyaa15rosee')



pCalc.calculateAllPayoffs()
#pCalc.loadPayoffs()
#print b
#k=0
#pCalc.calculateIndividualPayoff('doritos', tags, 5)
pCalc.dumpPayoffs()
input('')
#pCalc.loadPayoffs()
#lol=0