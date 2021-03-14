import sys
import zmq
from threading import Thread
import random
import time
from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging

#logging required by zookeeper
logging.basicConfig()

class subscriber(Thread):

	def __init__(self, topic, flood, broker_add):
		super().__init__()
		self.topic = topic
		self.flood = flood
		self.joined = True
		self.context = zmq.Context()
		self.sub = self.context.socket(zmq.SUB)
		self.sub.setsockopt_string(zmq.SUBSCRIBE, self.topic)

		#zk initializing
		self.path = '/leader/node'
		self.broker = broker_add
		self.zk_object = KazooClient(hosts='127.0.0.1:2181')
		self.zk_object.start()
		
		
		if self.flood == True:
			for i in range(1,6):
				port = str(5558 + i)
				self.sub.connect("tcp://127.0.0.1:" + port)
		else:
			data, stat = self.zk_object.get(self.path)
			data = str(data)
			addr = data.split(",")
			addr[1] = addr[1][:-1]
			print("tcp://" + self.broker + ":" + addr[1])	
			self.sub.connect("tcp://" + self.broker + ":" + addr[1])

	def run(self):
		print('starting sub ' + self.topic)
		while self.joined:
			@self.zk_object.DataWatch(self.path)
			def watch_node(data, stat, event):
				if event != None:	
					#if broker fails - restart self + reconnect
					if event.type == "CHANGED":
						self.sub.close()
						self.connext.term()
						time.sleep(2)
						self.context = zmq.Context()
						self.sub = self.context.socket(zmq.SUB)
						#reconnect to broker
						data, stat = self.zk_object.get(self.path)
						data = str(data)
						addr = data.split(",")
						addr[1] = addr[1][:-1]
						self.sub.connect("tcp://" + self.broker + ":" + addr[1])

			string = self.sub.recv()
			topic, messagedata = string.split()
			print (topic, messagedata)

	def close(self):
		self.sub.close()
		print('sub ' + self.topic + ' leaving')

class publisher(Thread):

	def __init__(self, id, flood, broker_add):
		super().__init__()
		self.id = id
		self.flood = flood
		self.joined = True

		#connect to the lead broker and start zk watch
		self.broker = broker_add
		self.path = '/leader/node'
		self.zk_object = KazooClient(hosts='127.0.0.1:2181')
		self.zk_object.start()

		self.context = zmq.Context()
		self.pub = self.context.socket(zmq.PUB)
		if self.flood == True:
			self.pub.bind("tcp://127.0.0.1:" + str(5558 + self.id))
		else:
			data, stat = self.zk_object.get(self.path)
			data = str(data)
			addr = data.split(",")
			addr[0] = addr[0][2:]
			print("tcp://" + self.broker + ":" + addr[0])
			self.pub.connect("tcp://" + self.broker + ":" + addr[0])



	def run(self):
		print('starting publisher number ' + str(self.id))
		#select a stock
		stock_list = ["GOOG", "AAPL", "MSFT", "IBM", "AMD", "CLII", "EXO", "NFLX", "CME", "CKA"]
		index = random.randrange(1,10)
		ticker = stock_list[index]
		print(self.pub)
		while self.joined:

			#watch for leader change
			@self.zk_object.DataWatch(self.path)
			def watch_node(data, stat, event):
				if event != None:	
				#if broker fails - restart self + reconnect
					if event.type == "CHANGED":
						self.pub.close()
						self.context.term()
						time.sleep(2)
						self.context = zmq.Context()
						self.pub = self.context.socket(zmq.PUB)
						data, stat = self.zk_object.get(self.path)
						data = str(data)
						addr = data.split(",")
						addr[0] = addr[0][2:]
						self.pub.connect("tcp://" + self.broker + ":" + addr[0])

			#generate a random price
			price = str(random.randrange(20, 60))
			#send ticker + price to broker
			self.pub.send_string("%s %s" % (ticker, price))
			time.sleep(1)

	def close(self):
		self.pub.close()
		print('pub leaving')

class listener(Thread):
	
	#init self
	def __init__(self, flood):
		super().__init__()
		self.flood = flood
		self.joined = True

	#start up the thread
	def run(self):
		print("starting listener thread")
		context = zmq.Context()
		sub = context.socket(zmq.SUB)
		#Flooding version - connect to all pub networks w/o a filter
		if self.flood == True: 
			for i in range(1,8):
				port = str(5558 + i)
				sub.connect("tcp://127.0.0.1:" + port)
				sub.setsockopt_string(zmq.SUBSCRIBE, "")
		#Broker version - connect w/o filtering
		else:
			sub.connect("tcp://127.0.0.1:5559")
			sub.setsockopt_string(zmq.SUBSCRIBE, "")
		#make a list of messages and appended to it each time one arrives
		messages = []
		while self.joined:
			string = sub.recv()
			messages.append(messages)
			if (len(messages) % 10 == 0):
				print(str(len(messages)) + " messages sent by brokers")
			
#initializing the individual pubs, sub, and listener
def main():

	s1 = subscriber('MSFT', False, '127.0.0.1')
	s1.start()

	s2 = subscriber('AAPL', False, '127.0.0.1')
	s2.start()

	s3 = subscriber('IBM', False, '127.0.0.1')
	s3.start()

	p1 = publisher(1, False, '127.0.0.1')
	p1.start()

	p2 = publisher(2, False, '127.0.0.1')
	p2.start()

	p3 = publisher(3, False, '127.0.0.1')
	p3.start()

if __name__ == "__main__":
    main()

