#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.clean import cleanup
from mininet.cli import CLI
import time

class SingleSwitchTopo(Topo):
	# "Single switch connected to n hosts."
	def __init__(self, n=2, **opts):

		# Initialize topology and default options
		Topo.__init__(self, **opts)
		switch = self.addSwitch('s1')

		# Python's range(N) generates 0...N-1
		for h in range(n):
			host = self.addHost('h%s'%(h+1))
		self.addLink(host, switch)

class MyFirstTopo(Topo):
	"Simple topology example."
	def __init__(self):
		"Create custom topo."
		#Initialize topology
		Topo.__init__(self)

		#Add hosts and switches
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')

		leftSwitch = self.addSwitch('s1')
		rightSwitch = self.addSwitch('s2')

		# Add links
		self.addLink(h1, leftSwitch)
		self.addLink(h2, leftSwitch)
		self.addLink(leftSwitch, rightSwitch)
		self.addLink(rightSwitch, h3)
		self.addLink(rightSwitch, h4)

	topos = {'myfirsttopo': (lambda: MyFirstTopo())}

def exampleBrokerTest():
	#"Create and test a simple network"
	topo = SingleSwitchTopo(n=4)
	net = Mininet(topo)
	net.start()
	print("Dumping host connections")
	dumpNodeConnections(net.hosts)
	print("Testing network connectivity")
	net.pingAll()
	net.stop()

def simpleTest():
	"Create and test a simple experiment"
	topo = MyFirstTopo()  							#Create an empty topology
	net = Mininet(topo, cleanup=True, xterms=True)  #Create the Mininet, start it and try some stuff
	net.start()

	net.pingAll()
	print("Pinging Test Complete")

	h1 = net.hosts[0]
	#h1.setIP('h1', '127.0.0.1', 8)
	#h1 = net.__getitem__('h1')
	print("h1 acquired")
	#TODO: Get the damn host to accept the shell commands to programmatically emulate
	h1.cmdPrint('xterm -xrm "python3 ./middleware/broker.py &" -T h1 &')
	#print(h1.cmd('python3 ./middleware/broker.py &'))
	print("h1 has been envoked as the broker")
	#print("Host", h1, "has IP address", net.IP('h1'))

	h2 = net.host("h2")
	h2.setIP('h2', '127.0.0.2', 8)
	print("h2 acquired")
	h2.sendCmd('python3 ./middleware/subscriber.py MSFT True &')
	print("Sent command to h2")
	#print("Host", h2.name, "has IP address", h2.IP())

	h3 = net.get("h3")
	h3.setIP('h3', "127.0.0.3", 8)
	print("h3 acquired")
	h3.sendCmd('python3 ./middleware/listener.py True &')
	print("Sent command to h3")
	#print("Host", h3.name, "has IP address", h3.IP())

	h4 = net.get("h4")
	h4.setIP('h4', '127.0.0.4', 8)
	print("h4 acquired")
	h4.sendCmd('python3 ./middleware/publisher.py 1 MSFT True &')
	print("Sent command to h4")
	#print("Host", h4.name, "has IP address", h4.IP())

	time.sleep(10)
	#net.stop()

	"""
	net.pingAll()
	net.iperf()
	"""

def simpleBrokerTest():
	#"Create and test a simple network"
	#topo = SingleSwitchTopo(n=4)
	#net = Mininet(topo)

	topo = Topo()
	topo.addSwitch("s1")  # Add switches and hosts to the topology
	topo.addHost("h1")
	topo.addHost("h2")
	topo.addHost("h3")
	topo.addHost("h4")
	topo.addLink("h1", "s1")  # Wire the switches and hosts together with links
	topo.addLink("h2", "s1")
	topo.addLink("h3", "s1")
	topo.addLink("h4", "s1")
	net = Mininet(topo)  # Create the Mininet, start it and try some stuff
	net.start()

	print("Starting host connections")
	#dumpNodeConnections(net.hosts)

	#Set the IPs for each of the hosts
	""""
	h1 = net.get("h1")
	print("h1 acquired")
	net.pingAll()
	result1 = h1.cmd('python3 ./middleware/broker.py')
	print("h1 has been envoked as the broker")
	print(result1)
	print("Host", h1.name, "has IP address", h1.IP())
	"""
	#h1.sendCmd('python3 ./middleware/broker.py')

	#TODO: How to connect hosts as h1, h2, and so on
	h2 = net.host("h2")
	print("h2 acquired")
	#net.pingAll()
	print("Pinging Test Complete")
	h2.cmd('python3 ./middleware/subscriber.py MSFT True')
	print("Sent command to h2")
	print("Host", h2.name, "has IP address", h2.IP())

	h3 = net.get("h3")
	h3.cmd('python3 ./middleware/listener.py True')
	print("Host", h3.name, "has IP address", h3.IP())

	h4 = net.get("h4")
	h4.cmd('python3 ./middleware/publisher.py 1 MSFT True')
	print("Host", h4.name, "has IP address", h4.IP())

	time.sleep(5)
	net.stop()

def complexBrokerTest():
	#"Create and test a simple network"
	topo = SingleSwitchTopo(n=4)
	net = Mininet(topo)
	net.start()
	print("Dumping host connections")
	dumpNodeConnections(net.hosts)
	print("Testing network connectivity")
	net.pingAll()
	net.stop()

def simpleFloodTest():
	#"Create and test a simple network"
	topo = SingleSwitchTopo(n=4)
	net = Mininet(topo)
	net.start()
	print("Dumping host connections")
	dumpNodeConnections(net.hosts)
	print("Testing network connectivity")
	net.pingAll()
	net.stop()

def complexFloodTest():
	#"Create and test a simple network"
	topo = SingleSwitchTopo(n=4)
	net = Mininet(topo)
	net.start()
	print("Dumping host connections")
	dumpNodeConnections(net.hosts)
	print("Testing network connectivity")
	net.pingAll()
	net.stop()

if __name__=='__main__':
	#Tell mininet to print useful information
	setLogLevel('info')
	##Test

	#Context Management
	##Cleanup previous runs
	cleanup()
	simpleTest()

	#Production
	##simpleBrokerTest()