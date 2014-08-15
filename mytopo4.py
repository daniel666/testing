#! /usr/bin/python

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

class Poisson:
    """Generate Poisson(lambda) values by using exponential
    random variables."""

    def __init__(self, lam):
        self.__lam = lam

    def nextPoisson(self):
        sum = 0
        n = -1
        while sum < self.__lam:
            n += 1
            sum -= math.log(random.random())
        return n

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )


	h1 = self.addHost('h1')
	h2 = self.addHost('h2')
	h3 = self.addHost('h3')
	h4 = self.addHost('h4')
	h5 = self.addHost('h5')
	h6 = self.addHost('h6')
	h7 = self.addHost('h7')
	h8 = self.addHost('h8')
	h9 = self.addHost('h9')
	h10 = self.addHost('h10')
	h11 = self.addHost('h11')
	h12 = self.addHost('h12')

	s1 = self.addSwitch( 's1', dpid = "0000000000000001" )
	s2 = self.addSwitch( 's2', dpid = "0000000000000002" )
	s3 = self.addSwitch( 's3', dpid = "0000000000000003" )
	s4 = self.addSwitch( 's4', dpid = "0000000000000004" )
	s5 = self.addSwitch( 's5', dpid = "0000000000000005" )
	s6 = self.addSwitch( 's6', dpid = "0000000000000006" )
	s7 = self.addSwitch( 's7', dpid = "0000000000000007" )
	s8 = self.addSwitch( 's8', dpid = "0000000000000008" )
	s9 = self.addSwitch( 's9', dpid = "0000000000000009" )
	s10 = self.addSwitch( 's10', dpid = "000000000000000a" )
	s11 = self.addSwitch( 's11', dpid = "000000000000000b" )
	s12 = self.addSwitch( 's12', dpid = "000000000000000c" )


	#link between hosts and switches

	self.addLink(s1, h1)
	self.addLink('s2', 'h2')
	self.addLink('s3', 'h3')
	self.addLink('s4', 'h4')
	self.addLink('s5', 'h5')
	self.addLink('s6', 'h6')
	self.addLink('s7', 'h7')
	self.addLink('s8', 'h8')
	self.addLink('s9', 'h9')
	self.addLink('s10', 'h10')
	self.addLink('s11', 'h11')
	self.addLink('s12', 'h12')


	#link between switches

	self.addLink('s1', 's2')
	self.addLink('s1', 's3')
	self.addLink('s1', 's4')
	self.addLink('s2', 's5')
	self.addLink('s2', 's3')
	self.addLink('s3', 's6')
	self.addLink('s3', 's7')
	self.addLink('s3', 's4')
	self.addLink('s4', 's8')
	self.addLink('s5', 's9')
	self.addLink('s5', 's6')
	self.addLink('s5', 's8')
	self.addLink('s6', 's8')
	self.addLink('s6', 's7')
	self.addLink('s7', 's8')
	self.addLink('s8', 's9')
	self.addLink('s8', 's10')
	self.addLink('s8', 's11')
	self.addLink('s9', 's10')
	self.addLink('s10', 's11')
	self.addLink('s10', 's12')
	self.addLink('s11', 's12')

CONTROLLERS = { 'ref': Controller,
                'ovsc': OVSController,
                'nox': NOX,
                'remote': RemoteController,
                'none': lambda name: None }
ADD_SLEEP_T = 2
REMOVE_SLEEP_T = 2
#multicastGroup = ['h1','h2','h3','h4', 'h5','h6','h7','h8','h9','h10','h11','h12']
##for i in range(1,13):
    ##multicastGroup.append('h'+ str(i))
#multicastLeave = ['h2','h3','h4', 'h5','h6','h7','h8','h9','h10','h11','h12']

#print "multicastGroup", multicastGroup
#print "multicastLeave", multicastLeave

operations=[1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
operationNodes=['h1','h2','h3','h4', 'h5','h6','h7','h8','h9','h10','h11','h12','h2','h3','h4', 'h5','h6','h7','h8','h9','h10','h11','h12']

setLogLevel( 'info' )
topo = MyTopo()
remotecontroller = customConstructor(CONTROLLERS, "remote,ip=192.168.56.1")
net = Mininet(topo = topo, controller=remotecontroller)
net.start()
for host in net.hosts:
    host.cmdPrint('route add default dev %s-eth0' %host.name)
time.sleep(5)

for i in range(len(operations)):
    if operations[i] == 1:
        hostname = operationNodes[i]
        print "%s is ready to join" % hostname
        host = net.get(hostname)
        host.cmdPrint('iperf -s -u -B 224.0.55.55 &')
        time.sleep(ADD_SLEEP_T)
    else:
        hostname = operationNodes[i]
        print "%s is ready to leave and its last pid  is %s" % (hostname, host. lastPid)
        host = net.get(hostname)
        cmd = "kill %s" % host.lastPid
        host.cmd(cmd)
        time.sleep(REMOVE_SLEEP_T)


#for hostname in multicastGroup:
    #print "%s is ready to join" % hostname
    #host = net.get(hostname)
    #host.cmdPrint('iperf -s -u -B 224.0.55.55 &')
    #time.sleep(ADD_SLEEP_T)
#for hostname in multicastLeave:
    #host = net.get(hostname)
    #print "%s is ready to leave and its last pid  is %s" % (hostname, host. lastPid)
    #cmd = "kill %s" % host.lastPid
    #host.cmd(cmd)
    #time.sleep(REMOVE_SLEEP_T)

net.stop()
#topos = { 'mytopo': ( lambda: MyTopo() ) }


