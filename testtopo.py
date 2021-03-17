from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time
from mininet.cli import CLI
tree4 = TreeTopo(depth=2,fanout=2)
net = Mininet(topo=tree4, cleanup=True, xterms=True)
net.start()
h1, h4 = net.hosts[0], net.hosts[3]

#CLI(net, do_sh='h1 python3 ./middleware/broker.py &')

h1.cmd('xterm -xrm "python3 ./middleware/broker.py &" -T h1 &')
#h1.pexec('h1 python3 ./middleware/broker.py &')
#h1.run('ping -c1 %s' % h4.IP())

time.sleep(10)
net.stop()