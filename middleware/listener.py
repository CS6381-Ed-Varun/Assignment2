import sys
import zmq
from threading import Thread
import random
import time

class listener(Thread):

    # init self
    def __init__(self, flood):
        super().__init__()
        self.flood = flood
        self.joined = True
        self.broker = broker_add
        self.path = '/leader/node'
        # port from zk config file, host ip should be changed
        self.zk_object = KazooClient(hosts='127.0.0.1:2181')
        self.zk_object.start()

    # start up the thread
    def run(self):
        print("starting listener thread")
        context = zmq.Context()
        sub = context.socket(zmq.SUB)
        #print('Flood variable is ' + self.flood)
        # Flooding version - connect to all pub networks w/o a filter
        if self.flood != True:
            #print('Flooding Approach is being monitored')
            for i in range(1, 8):
                port = str(5558 + i)
                sub.connect("tcp://10.0.0." + str(i) + ":" + port)
                sub.setsockopt_string(zmq.SUBSCRIBE, "")
        # Broker version - connect w/o filtering
        else:
            data, stat = self.zk_object.get(self.path)  # get port #'s from the leader's zk node
            data = str(data)
            addr = data.split(",")  # type casting since path is bytes and strings are needed for connect
            addr[0] = addr[0][2:]  # removing a ' from the byte -> string cast
            print("tcp://" + self.broker + ":" + addr[0])
            self.sub.connect("tcp://" + self.broker + ":" + addr[0])  # connecting to the broker
            #sub.setsockopt_string(zmq.SUBSCRIBE, "")
            print('Broker Approach is being listened to')
            #sub.connect("tcp://10.0.0.1:5559")
            sub.setsockopt_string(zmq.SUBSCRIBE, "")
        # make a list of messages and appended to it each time one arrives
        messages = []
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
            string = sub.recv()
            messages.append(messages)
            if (len(messages) % 10 == 0):
                print(str(len(messages)) + " messages sent by brokers")

    def close(self):
        self.joined = False
        print('listener leaving')

def main():
    method = sys.argv[1]

    lis = listener(method)
    lis.start()
    #while True:
        #lis.start()

if __name__=='__main__':
    main()