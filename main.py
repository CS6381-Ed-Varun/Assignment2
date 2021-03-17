import sys
import zmq
from threading import Thread
import random
import time

import middleware
from middleware.publisher import publisher
from middleware.subscriber import subscriber
from middleware.listener import listener
from middleware import broker

#initializing the individual pubs, sub, and listener
def main():

	s1 = middleware.subscriber('MSFT', True)
	s1.start()

	s2 = middleware.subscriber('AAPL', True)
	s2.start()

	s3 = middleware.subscriber('IBM', True)
	s3.start()

	p1 = middleware.publisher(1, 'MSFT', True)
	p1.start()

	p2 = middleware.publisher(2, 'AAPL', True)
	p2.start()

	p3 = middleware.publisher(3, 'IBM', True)
	p3.start()

	l1 = middleware.listener(True)
	l1.start()

	time.sleep(5)
	p3.leave()

if __name__ == "__main__":
    main()