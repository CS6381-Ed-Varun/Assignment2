import sys
import zmq
from threading import Thread
import datetime
import os
import random
import time

class subscriber(Thread):

	def __init__(self, topic, flood, broker_add):
		super().__init__()
		self.topic = topic
		self.flood = flood
		self.joined = True

		# connect to the socket like normal. self.sub = our sub socket
		self.context = zmq.Context()
		self.sub = self.context.socket(zmq.SUB)
		self.sub.setsockopt_string(zmq.SUBSCRIBE, self.topic)

		# initializing zookeeper
		self.path = '/leader/node'
		# setting the broker ip which is 'known' so we can use it as an input
		self.broker = broker_add
		# where zk is hosted - change local host part as needed and port 2181 comes from the config file
		self.zk_object = KazooClient(hosts='127.0.0.1:2181')
		self.zk_object.start()

		# flooding connection
		if self.flood == True:
			for i in range(1, 6):
				port = str(5558 + i)
				self.sub.connect("tcp://127.0.0.1:" + port)
		# connecting tp the broker using zookeeper node on leader broker
		else:
			data, stat = self.zk_object.get(self.path)  # get port #'s from the leader's zk node
			data = str(data)
			addr = data.split(",")  # type casting since path is bytes and strings are needed for connect
			addr[0] = addr[0][2:]  # removing a ' from the byte -> string cast
			print("tcp://" + self.broker + ":" + addr[0])
			self.sub.connect("tcp://" + self.broker + ":" + addr[0])  # connecting to the broker

	def run(self):
		print('starting sub ' + self.topic)
		print('Flood variable is ' + self.flood)
		if self.flood != True:
			print('Flooding Approach Enabled for Subscriber')
			for i in range(1, 8):
				port = str(5558 + i)
				# FIXME: Edit the binding to seek the appropriate IP 10.0.0.#
				print("tcp://10.0.0.{ipid}:{portid}".format(ipid=i, portid=port))
				sub.connect("tcp://10.0.0.{ipid}:{portid}".format(ipid=i, portid=port))
				#sub.connect("tcp://10.0.0.{ipid}:{portid}".format(ipid=i, portid=port) + str(i) + ":" + port)
				sub.setsockopt_string(zmq.SUBSCRIBE, self.topic)
		else:
			print('Broker Approach Enabled for Subscriber')
			sub.connect("tcp://10.0.0.1:5559")
			sub.setsockopt_string(zmq.SUBSCRIBE, self.topic)
		while self.joined:
			# setting our zk watch on the broker node
			@self.zk_object.DataWatch(self.path)
			def watch_node(data, stat, event):
				# required to allow us to check the type lower down
				if event != None:
					# if anything happens to the znode: close the connections, sleep, and then reconnect using new leader ports
					if event.type == "CHANGED":
						self.sub.close()
						self.context.term()
						time.sleep(2)
						self.context = zmq.Context()
						self.sub = self.context.socket(zmq.SUB)
						# reconnect to broker
						data, stat = self.zk_object.get(self.path)
						data = str(data)
						addr = data.split(",")  # same type casting as above for bytes -> string
						addr[0] = addr[0][2:]
						self.sub.connect("tcp://" + self.broker + ":" + addr[0])
			string = sub.recv_string()
			topic, price, time_started = string.split()

			#time_received = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
			#time_received = (datetime.datetime.now().strftime("%H:%M:%S.%f"))
			time_received = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
			latency = format((1000*(float(time_received) - float(time_started))), '.5f')
			print(topic, price, latency, 'ms')
			with open("./results/latency_{}.csv".format(topic), "a") as f:
				f.write(str(latency) + "\n")

	def leave(self):
		self.joined = False
		print('sub ' + self.topic + ' leaving')

def main():
	topic = sys.argv[1]
	method = sys.argv[2]

	if not str(topic) or len(topic) != 4:
		print("Invalid Stock Ticker")
		sys.exit(-1)

	#Should try to check whether method is boolean

	sub = subscriber(topic, method)
	sub.start()
	#while True:
		#sub.start()
		#time.sleep(1)

if __name__=='__main__':
	main()