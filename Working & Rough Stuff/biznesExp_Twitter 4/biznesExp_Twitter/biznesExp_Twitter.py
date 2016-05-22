from Headers.TwitterCommunicator import *
from Headers.Payoff.PayoffCalculator import *
from Headers.Payoff.DataCruncher import *
from Headers.Payoff.GoogleScraper import *
from Headers.NetworkData import *

import networkx as nx
import math
import matplotlib.pyplot as plt

def allCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in allCombinations(items[i+1:],n-1):
                yield [items[i]]+cc


def findPotentialAdopters(graph, numAdopters):
    for v in graph:
        lol=0


def draw_graph(graph, layout):
    plt.figure()
    nodes = graph.nodes()
    colors = ['r' if graph.node[n]['choice'] == 'A' else 'b'
              for n in graph]
    plt.axis('off')
    nx.draw_networkx(graph, nodelist=nodes, with_labels=True,
                     width=1, node_color=colors,alpha=.5,
                     pos=layout)

def setAdopters(graph, adopters):
    for a in adopters:
        graph.node[a]['choice']='A'


def doCascade(graph, adopters):
    #draw_graph(graph, nx.spring_layout(graph))
    #plt.show()
    newAdopters = 0

    for v in graph:
        if graph.node[v]['choice'] == 'B':
            a_neighbors = [w for w in graph.neighbors(v)
                           if graph.node[w]['choice'] == 'A']
            b_neighbors = [w  for w in graph.neighbors(v)
                           if graph.node[w]['choice'] == 'B']
            p = 1. * len(a_neighbors) / (len(a_neighbors) + len(b_neighbors))
            q = 1 - graph.node[v]['payoff']
            if p >= q:
                graph.node[v]['choice'] = 'A'
                newAdopters = newAdopters + 1
        #else:
            #graph.node[v]['choice'] = 'B'

        #draw_graph(graph, nx.spring_layout(graph))
        #plt.show()

    #draw_graph(graph, nx.spring_layout(graph))
    #plt.show()
    return newAdopters


tags = ['celebrity', 'famous', 'party']
numAdopters = 6

nData = NetworkData()
nData.loadFriendNetworkData('dump_friendNetworks_prev.txt')
pCalc = PayoffCalculator(nData, tags)
pCalc.loadPayoffs()
for key in pCalc.payOffs.keys():
     if math.isnan(pCalc.payOffs[key]) or pCalc.payOffs[key] == 0:
         del pCalc.payOffs[key]
sortedPayOffsList = sorted(pCalc.payOffs.iteritems(), key=lambda (k, v): (-v, k))[:]

lol=0

friendGraph = nx.Graph()

for friend in pCalc.payOffs.keys():
    friendsOfFriend_tObjects = list(nData.friendNetworks[friend].get_iterator())
    friendsOfFriend_snames = [k['screen_name'] for k in friendsOfFriend_tObjects]
    myOtherFriends_snames = list(pCalc.payOffs.keys())
    myOtherFriends_snames = [x for x in myOtherFriends_snames if x is not friend]
    for f in friendsOfFriend_snames:
        if f in myOtherFriends_snames:
            friendGraph.add_edge(friend, f)

nx.set_node_attributes(friendGraph, 'payoff', 0.)
nx.set_node_attributes(friendGraph, 'choice', 'B') #Choice 'A' is positive & 'B' is negative.

for n in friendGraph.nodes():
    friendGraph.node[n]['payoff'] = pCalc.payOffs[n]

clusters = list(nx.connected_component_subgraphs(friendGraph))
cluster_sizes = [len(c.nodes()) for c in clusters]
cluster_sizeMap = zip(clusters, cluster_sizes)
clusterCount = len(clusters)

for cluster in clusters:
    ad = cluster.nodes()[0:15]

    l = nx.spring_layout(friendGraph)

    setAdopters(cluster, ad)

    #draw_graph(cluster, nx.spring_layout(cluster))
    #plt.show()

    while True:
        newAdopters = doCascade(cluster, ad)
        print newAdopters
        if newAdopters == 0:
            break

    #draw_graph(cluster, nx.spring_layout(cluster))
    #plt.show()
    lol=0

lol=0