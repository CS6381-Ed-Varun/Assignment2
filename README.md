# CS6381 Assignment2


# CS6381 Programming Assignment #1

## Overview
In this assignment we will build upon the PUB/SUB model supported by the ZeroMQ (ZMQ) middleware. 
One of the downsides of ZMQ’s approach is that there is no anonymity between publishers and subscribers. 
A subscriber needs to know where the publisher is (i.e., subscriber must explicitly connect to a publisher using its IP address and port). 
So, we lose some degree of decoupling with such an approach (recall the time, space, and synchronization decoupling that we studied). 
A more desirable solution is where application logic of the publishers and subscribers remains anonymous to each other; 
naturally something else will still need to maintain the association. 
This entity is the pub-sub middleware, which is the focus of this assignment. 

| Simple Broker Latency                                                                                                    | Complex Broker Latency                                                                                                     | Simple Flooding Latency                                                                                                      | Complex Flooding Latency                                                                                                       |
|--------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| ![simple_broker](https://github.com/edmasters/single_broker_pub_sub/blob/automated-local-host/results/simple_broker.png) | ![complex_broker](https://github.com/edmasters/single_broker_pub_sub/blob/automated-local-host/results/complex_broker.png) | ![simple flooding](https://github.com/edmasters/single_broker_pub_sub/blob/automated-local-host/results/simple_flooding.png) | ![complex flooding](https://github.com/edmasters/single_broker_pub_sub/blob/automated-local-host/results/complex_flooding.png) |

## Installation
Activate the Python Environment Variables:
```bash
source env/bin/activate
```

To deactivate the Python Environment Variables:
```bash
deactivate
```

Manual installation: 
```bash
git clone https://github.com/edmasters/single_broker_pub_sub.git
cd single_broker_pub-sub
```

If you have `pip` installed, then
```bash
pip install -e .
```

If you do not have `pip`, then
```bash
python setup.py install
```
Activate the Python Environment Variables:
```bash
source env/bin/activate
```
## Mininet Emulation
Assign the various hosts as either publisher or subscriber. 
Subsequently, passing the parameters for the stock ticker and API method will generate the connections.
The latencies will be exported to a csv and an analysis can be replicated with offline_analysis.py

### Simple Broker Approach
```bash
sudo mn -c #For cleaning up the environment
sudo mn --topo single,4 -x
mininet> h1 python3 ./middleware/broker.py &
mininet> h2 python3 ./middleware/subscriber.py AAPL True &
mininet> h3 python3 ./middleware/listener.py True &
mininet> h4 python3 ./middleware/publisher.py 1 AAPL True &
```

### Complex Broker Approach
```bash
sudo mn -c #For cleaning up the environment
sudo mn --topo single,8 -x
mininet> h1 python3 ./middleware/broker.py &
mininet> h2 python3 ./middleware/subscriber.py AAPL True &
mininet> h3 python3 ./middleware/subscriber.py MSFT True &
mininet> h4 python3 ./middleware/subscriber.py NFLX True &
mininet> h5 python3 ./middleware/publisher.py 5 AAPL True &
mininet> h6 python3 ./middleware/publisher.py 6 MSFT True &
mininet> h7 python3 ./middleware/publisher.py 7 NFLX True &
mininet> h8 python3 ./middleware/listener.py True &
```

### Simple Flood Approach
```bash
sudo mn -c #For cleaning up the environment
sudo mn --topo single,4 -x
mininet> h1
mininet> h2 python3 ./middleware/subscriber.py AAPL False &
mininet> h3 python3 ./middleware/listener.py False &
mininet> h4 python3 ./middleware/publisher.py 4 AAPL False &
```

### Complex Flood Approach
```bash
sudo mn -c #For cleaning up the environment
sudo mn --topo single,8 -x
mininet> h1 python3 ./middleware/subscriber.py AAPL False &
mininet> h2 python3 ./middleware/subscriber.py MSFT False &
mininet> h3 python3 ./middleware/subscriber.py NFLX False &
mininet> h4 python3 ./middleware/publisher.py 4 AAPL False &
mininet> h5 python3 ./middleware/publisher.py 5 MSFT False &
mininet> h6 python3 ./middleware/publisher.py 6 NFLX False &
mininet> h7 python3 ./middleware/listener.py False &
```

## Rubric

