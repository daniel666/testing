"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

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

	s1 = self.addSwitch( 's1', dpid = "0000000000000001" )
	s2 = self.addSwitch( 's2', dpid = "0000000000000002" )
	s3 = self.addSwitch( 's3', dpid = "0000000000000003" )
	s4 = self.addSwitch( 's4', dpid = "0000000000000004" )

	self.addLink('s1', 'h1')
	self.addLink('s1', 'h2')
	self.addLink('s1', 's2')
	self.addLink('s1', 's3')
	self.addLink('s2', 'h3')
	self.addLink('s2', 'h4')
	self.addLink('s2', 's4')
	self.addLink('s3', 'h5')
	self.addLink('s3', 'h6')
	self.addLink('s3', 's4')
	self.addLink('s4', 'h7')
	self.addLink('s4', 'h8')

        # Add hosts and switches
        #leftHost = self.addHost( 'h1' )
        #rightHost = self.addHost( 'h2' )
        #leftSwitch = self.addSwitch( 's3' )
        #rightSwitch = self.addSwitch( 's4' )

	# Add links
        #self.addLink( leftHost, leftSwitch )
        #self.addLink( leftSwitch, rightSwitch )
        #self.addLink( rightSwitch, rightHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }
