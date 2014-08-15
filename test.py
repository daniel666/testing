#! /usr/bin/python
# coding: utf-8
from subprocess import call
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, Controller, OVSController, NOX
from mininet.cli import CLI
#from mininet.log import MininetLogger.setLogLevel
from mininet.log import setLogLevel, info
from mininet.util import custom, customConstructor
from mininet.util import buildTopo

import time
import os
import random
import sys

from britetopo import MyBriteTopo



CONTROLLERS = { 'ref': Controller,
                'ovsc': OVSController,
                'nox': NOX,
                'remote': RemoteController,
                'none': lambda name: None }
#LOW = 1
#HIGH = 1000
#NUM_ADD = 300
#NUM_REMOVE = 100

LOW = 1
HIGH = 500
NUM_ADD = 300
NUM_REMOVE = 100

SLEEP_TIME = 10
ADD_SLEEP_T = 2
REMOVE_SLEEP_T = 2
#multicastGroup = map(lambda x: 'h'+ str(x),  random.sample(range(LOW, HIGH), NUM_ADD))
#multicastLeave = map(lambda x: multicastGroup[x], random.sample(range(NUM_ADD), NUM_REMOVE))
#multicastGroup = []
#multicastLeave = []
#print "multicastGroup:", multicastGroup
#print "multicastLeave:", multicastLeave

terminals = []
nonterminals = []
operations = []
operationNodes = []
eventqueue = []

class Update:
    def __init__(self, node, typename, time):
        self.__node = node
        self.__typename = typename
        self.__time = time

    def __repr__(self):
        return "<%s, %s, %s>" %(time, typename, node)


class LifetimeGen:
    def __init__(self):
        return 50

#class Poisson:
    #"""Generate Poisson(lambda) values by using exponential
    #random variables."""

    #def __init__(self, lam):
        #self.__lam = lam

    #def nextPoisson(self):
        #sum = 0
        #n = -1
        #while sum < self.__lam:
            #n += 1
            #sum -= math.log(random.random())
        #return n

    #def nextArrivalTime(self):
        #-(math.log(1.0-random.random())/self.__lam


def doSimulation():
    rate = 6 # 6 add per 10s
    numRound = 50 # 50 rounds
    ROUND_TIME = 10
    END_TIME = 500
    eventGen = Poisson(rate)
    lifetimeGen = LifetimeGen()
    #for round in range(numRound):
        #numAddEvent = eventGen.nextPoisson()
        #starttime = round*ROUND_TIME
        #for i in range(numAddEvent):
            #node = nonterminals.choice()
            #nonterminals.remove(node)
            #eventqueue.add(Update(node, "add", starttime))
            #lifetime = lifetimeGen.getlifetime()
            #eventqueue.add(Update(node), "remove", starttime+lifetime)
            #starttime += eventGen.nextArrivalTime()
    starttime = 0
    while starttime <= END_TIME:
        node = nonterminals.choice()
        nonterminals.remove(node)
        eventqueue.add(Update(node, "add", starttime))
        lifetime = lifetimeGen.getlifetime()
        eventqueue.add(Update(node, "remove", starttime+lifetime))
        starttime += eventGen.nextArrivalTime()
    eventqueue = sorted(eventqueue, key = lambda update: update.starttime)

    time = 0
    for event in eventqueue:
        while(time <= event.time):
            sleep(1)
            time += 1
        if event.type == "add":
            addhost = event.node
            host = net.get(addhost)
            print "%s is ready to join" % addhost
            host.cmdPrint('iperf -s -u -B 224.0.55.55 &')

        if event.type == "remove":
            removehost = event.node
            host = net.get(removehost)
            print "%s is ready to leave and its last pid  is %s" % (removehost, host.lastPid)
            cmd = "kill %s" % host.lastPid
            host.cmd(cmd)
    print eventqueue


def myNetSimulation():
    #call(['sudo', 'mn', '-c'])
    global terminals
    global nonterminals

    nonterminals = map(lambda x: 's'+str(int(x+1)), range(HIGH))
    terminals = []
    britefile =  sys.argv[1] if len(sys.argv) >=2 else None
    topo = MyBriteTopo(britefile)
    remotecontroller = customConstructor(CONTROLLERS, "remote,ip=192.168.56.1")
    net = Mininet(topo = topo, controller=remotecontroller)
    net.start()    #启动您的拓扑网络
    for host in net.hosts:
        host.cmdPrint('route add default dev %s-eth0' %host.name)
    time.sleep(SLEEP_TIME)
    doSimulation()




def generateOps():
    global NUM_ADD
    global NUM_REMOVE
    global terminals
    global operations
    global operationNodes
    operations =  [1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1,-1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1]
    operationNodes =  ['h19', 'h164', 'h91', 'h6', 'h198', 'h230', 'h198', 'h94', 'h248', 'h164', 'h132', 'h130', 'h6', 'h71', 'h191', 'h26', 'h169', 'h133', 'h112', 'h94', 'h130', 'h150', 'h133', 'h169', 'h167', 'h191', 'h71', 'h70', 'h51', 'h150', 'h34', 'h97', 'h170', 'h51', 'h223', 'h41', 'h236', 'h68', 'h41', 'h165', 'h177', 'h240', 'h204', 'h167', 'h5', 'h204', 'h163', 'h250', 'h241', 'h132', 'h6', 'h150', 'h73', 'h70', 'h241', 'h165', 'h121', 'h126', 'h134', 'h118', 'h223',
            'h81', 'h62', 'h81', 'h179', 'h65', 'h41', 'h170', 'h101', 'h163', 'h79', 'h3', 'h233', 'h39', 'h127', 'h99', 'h20', 'h200', 'h121', 'h48', 'h41', 'h160', 'h144', 'h84', 'h2', 'h173', 'h150', 'h12', 'h129', 'h57', 'h248', 'h129', 'h68', 'h123', 'h232', 'h1', 'h166', 'h82', 'h144', 'h177', 'h78', 'h133', 'h164', 'h75', 'h50', 'h236', 'h126', 'h155', 'h140', 'h114', 'h87', 'h80', 'h250', 'h237', 'h22', 'h128', 'h8', 'h72', 'h226', 'h44', 'h20', 'h100', 'h57', 'h217', 'h123','h91', 'h36', 'h239', 'h198', 'h171', 'h10', 'h227', 'h161', 'h165', 'h74', 'h86', 'h164', 'h201', 'h152', 'h76', 'h247', 'h134', 'h185', 'h57', 'h74', 'h210', 'h248', 'h78', 'h166', 'h12', 'h160', 'h69', 'h29', 'h120', 'h196', 'h124', 'h230', 'h200', 'h196', 'h44', 'h93', 'h181', 'h214', 'h101', 'h132', 'h36', 'h154', 'h234', 'h212', 'h182', 'h43', 'h92', 'h56', 'h71', 'h218', 'h144', 'h94', 'h237', 'h13', 'h123', 'h237', 'h243', 'h110', 'h61', 'h156', 'h196', 'h202','h147', 'h70', 'h140', 'h151', 'h38', 'h247', 'h28', 'h63', 'h44', 'h216', 'h35', 'h250', 'h44']

    if not operations:
        print "operations:", operations
        print "operationNodes:", operationNodes
        return

    i = NUM_ADD + NUM_REMOVE
    print NUM_ADD, NUM_REMOVE
    PRO_ADD = NUM_ADD * 1.0/(NUM_ADD + NUM_REMOVE)
    while(i > 0):
        prob = random.random()
        print prob, PRO_ADD
        if(prob<PRO_ADD):
            operations.append(1)
            node = 'h'+ str(random.randint(1, HIGH))
            while(node in terminals):
                node = 'h'+ str(random.randint(1, HIGH))
            operationNodes.append(node)
            terminals.append(node)
            i = i - 1
            print "add nodes ", node
        else:
            if(not terminals):
                continue
            #prevent from cost jumpting to zero
            if(len(terminals) <= 5):
                continue
            removenode = random.choice(terminals)
            while(removenode == terminals[0]):
                removenode = random.choice(terminals)
            operations.append(-1)
            operationNodes.append(removenode)
            terminals.remove(removenode)
            i = i -1
            print "remove nodes ", removenode

    print "operations:", operations
    print "operationNodes:", operationNodes


def myNet():
    #call(['sudo', 'mn', '-c'])
    britefile =  sys.argv[1] if len(sys.argv) >=2 else None
    print "britefile:",  britefile
    generateOps()


    topo = MyBriteTopo(britefile)
    remotecontroller = customConstructor(CONTROLLERS, "remote,ip=192.168.56.1")
    net = Mininet(topo = topo, controller=remotecontroller)
    net.start()    #启动您的拓扑网络
    for host in net.hosts:
        host.cmdPrint('route add default dev %s-eth0' %host.name)
    time.sleep(SLEEP_TIME)

    for i in range(len(operations)):
        if(operations[i] == 1):
            addhost = operationNodes[i]
            host = net.get(addhost)
            print "%s is ready to join" % addhost
            host.cmdPrint('iperf -s -u -B 224.0.55.55 &')
            time.sleep(ADD_SLEEP_T)
        else:
            removehost = operationNodes[i]
            host = net.get(removehost)
            print "%s is ready to leave and its last pid  is %s" % (removehost, host.lastPid)
            cmd = "kill %s" % host.lastPid
            host.cmd(cmd)
            time.sleep(REMOVE_SLEEP_T)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()

