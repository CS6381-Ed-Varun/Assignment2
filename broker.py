
import zmq
import os
import sys
import time
import threading
import zmq
from random import randrange
from ansible.module_utils._text import to_bytes
from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging

logging.basicConfig()

class broker:

	def __init__(self):
		#setting up proxy
		self.context = zmq.Context()
		self.frontend = self.context.socket(zmq.XPUB)
		self.backend = self.context.socket(zmq.XSUB)

		#zookeeper nodes
		self.zk_object = KazooClient(hosts='127.0.0.1:2181')
		self.zk_object.start()
		self.path = '/home/'

		#znode for each broker
		node1 = self.path + "broker1"
		if self.zk_object.exists(node1):
			pass
		else:
			#make sure the path exists
			self.zk_object.ensure_path(self.path)
			#create the znode with port info for the pubs + subs to use in addr[]
			self.zk_object.create(node1, to_bytes("5555,5556"))

		#znode2 (same w/ modified port #'s')
		node2 = self.path + "broker2"
		if self.zk_object.exists(node2):
			pass
		else:
			#make sure the path exists
			self.zk_object.ensure_path(self.path)
			#create the znode with port info for the pubs + subs to use in addr[]
			self.zk_object.create(node2, to_bytes("5557,5558"))

		#znode 3
		node3 = self.path + "broker3"
		if self.zk_object.exists(node3):
			pass
		else:
			#make sure the path exists
			self.zk_object.ensure_path(self.path)
			#create the znode with port info for the pubs + subs to use in addr[]
			self.zk_object.create(node3, to_bytes("5559,5560"))

		#leader election among brokers (1st time)
		self.election = self.zk_object.Election(self.path, "leader")
		potential_leaders = self.election.contenders()
		self.leader = str(potential_leaders[-1])
		print("Leader ports: " + self.leader)

		#use port #'s from the leader to finish connecting the proxy'
		addr = self.leader.split(",")
		self.frontend.bind("tcp://*:" + addr[0])
		self.backend.bind("tcp://*:" + addr[1])

		#leader node creation + set-up
		self.watch_dir = self.path + self.leader
		self.leader_path ="/leader/"
		self.leader_node = self.leader_path + "node"
		if self.zk_object.exists(self.leader_node):
			pass
		#make if it doesn't exists
		else:
			self.zk_object.ensure_path(self.leader_path)
			self.zk_object.create(self.leader_node, ephemeral = True)

		#setting
		self.zk_object.set(self.leader_node, to_bytes(self.leader))

	def device(self):
		#start the proxy
		zmq.device(zmq.FORWARDER, self.frontend, self.backend)


	def monitor(self):
		while True:
			@self.zk_object.DataWatch(self.watch_dir)
			def watch_node(data, stat, event):
				#url's for unbinding later
				addr = self.leader.split(",")
				front_url = "tcp://*:" + addr[0]
				back_url = "tcp://*:" + addr[1]
				#re-elect leader if node is gone
				if event != None:
					if event.type == "DELETED":
						self.election = self.zk_object.Election(self.path, "leader")
						potential_leaders = self.election.contenders()
						self.leader = potential_leaders[-1].encode('latin-1')
						#reset node
						self.zk_object.set(self.leader_node, self.leader)

						#unbind + re-bind broker ports
						self.frontend.unbind(front_url)
						self.backend.unbind(back_url)
						self.frontend.bind("tcp://*:" + addr[0])
						self.backend.bind("tcp://*:" + addr[1])

			self.election.run(self.device)

if __name__ == "__main__":
    broker = broker()
    broker.monitor()
