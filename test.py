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
ADD_SLEEP_T = 5
REMOVE_SLEEP_T = 5
#multicastGroup = map(lambda x: 'h'+ str(x),  random.sample(range(LOW, HIGH), NUM_ADD))
#multicastLeave = map(lambda x: multicastGroup[x], random.sample(range(NUM_ADD), NUM_REMOVE))
#multicastGroup = []
#multicastLeave = []
#print "multicastGroup:", multicastGroup
#print "multicastLeave:", multicastLeave

terminals = []
operations = []
operationNodes = []

def generateOps():
    #for i in range(NUM_ADD + NUM_REMOVE):
    global NUM_ADD
    global NUM_REMOVE
    global terminals
    global operations
    global operationNodes
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
    call(['sudo', 'mn', '-c'])
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

