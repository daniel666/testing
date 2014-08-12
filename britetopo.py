"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
import re

class Switch():
	def __init__( self, strLine ):
		splitter = re.compile(r'([\t])')
		tokenArray = splitter.split(strLine)
		self.id =  str(int(tokenArray[0]) + 1)
		self.dpid = "00000000" + str("%08x" % int(self.id))
		print self.dpid

class Link():
	def __init__( self, strLine):
		splitter = re.compile(r'([\t])')
		tokenArray = splitter.split(strLine)
		self.srcId =str(int(tokenArray[2]) + 1)
		self.dstId = str(int(tokenArray[4]) + 1)

class MyBriteTopo( Topo ):
    "Simple topology example."
    #srcfile = "/home/mininet/out.brite"
    configFile = "/home/mininet/britetopo.conf"

    def __init__( self , srcfile = '/home/mininet/out.brite'):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

	ins = open(srcfile, "r" )
	ins.readline()
	ins.readline()
	ins.readline()

	numNodeLine = ins.readline()
	splitter = re.compile(r'([() ])')
	tmp = splitter.split(numNodeLine)
	numNodes = int(tmp[6])
	switchesArray= []
	for x in range(0, numNodes):
		switch = Switch(ins.readline())
		switchesArray.append(switch)
	ins.readline()
	ins.readline()
	linksArray = []
	tmp2 = splitter.split(ins.readline())
	numLinks = int(tmp2[6])
	for x in range(0, numLinks):
	    link = Link(ins.readline())
	    linksArray.append(link)
	ins.close()

	###
	### add links and switches and hosts
	for switch in switchesArray:
		self.addSwitch('s'+ switch.id, dpid=switch.dpid)
		#self.addSwitch('s'+ switch.id)
		opt ={'defaultRoute':"h%s-eth0" %switch.id}
		#self.addHost('h%s'%switch.id, opt)
		self.addHost('h%s'%switch.id, defaultRoute="h%s-eth0"%switch.id)
		self.addLink('s'+switch.id, 'h'+switch.id)

	for link in linksArray:
		self.addLink('s'+link.srcId, 's'+link.dstId)

	of = open(MyBriteTopo.configFile, 'w')
	for switch in switchesArray:
		of.write("h%s route add default dev h%s-eth0\n" %(switch.id, switch.id))
	of.close()

	# h1 = self.addHost('h1')
	# h2 = self.addHost('h2')
	# h3 = self.addHost('h3')
	# h4 = self.addHost('h4')
	# h5 = self.addHost('h5')
	# h6 = self.addHost('h6')
	# h7 = self.addHost('h7')
	# h8 = self.addHost('h8')

	# s1 = self.addSwitch( 's1', dpid = "0000000000000201" )
	# s2 = self.addSwitch( 's2', dpid = "0000000000000202" )
	# s3 = self.addSwitch( 's3', dpid = "0000000000000203" )
	# s4 = self.addSwitch( 's4', dpid = "0000000000000204" )

	# self.addLink('s1', 'h1')
	# self.addLink('s1', 'h2')
	# self.addLink('s1', 's2')
	# self.addLink('s1', 's3')
	# self.addLink('s2', 'h3')
	# self.addLink('s2', 'h4')
	# self.addLink('s2', 's4')
	# self.addLink('s3', 'h5')
	# self.addLink('s3', 'h6')
	# self.addLink('s3', 's4')
	# self.addLink('s4', 'h7')
	# self.addLink('s4', 'h8')

        # Add hosts and switches
        #leftHost = self.addHost( 'h1' )
        #rightHost = self.addHost( 'h2' )
        #leftSwitch = self.addSwitch( 's3' )
        #rightSwitch = self.addSwitch( 's4' )

	# Add links
        #self.addLink( leftHost, leftSwitch )
        #self.addLink( leftSwitch, rightSwitch )
        #self.addLink( rightSwitch, rightHost )


topos = { 'mytopo': ( lambda: MyBriteTopo() ) }
