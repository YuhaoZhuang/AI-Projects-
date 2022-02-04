import simpy
import math
import numpy as np
import random
import matplotlib.pyplot as plt
# First define some global variables. You should change values
class G:
    RANDOM_SEED = 33
    SIM_TIME = 1000 # This should be large
    SLOT_TIME = 1
    N = 10
    ARRIVAL_RATES = [0.001, 0.002, 0.003, 0.006, 0.012, 0.024] # Check the submission guidelines
    RETRANMISSION_POLICIES = ["pp", "op", "beb", "lb"]
    LONG_SLEEP_TIMER = 1000000000
class Server_Process(object):
    def __init__(self, env, dictionary_of_nodes, retran_policy, slot_stat):
        self.env = env
        self.dictionary_of_nodes = dictionary_of_nodes
        self.retran_policy = retran_policy
        self.slot_stat = slot_stat
        self.current_slot = 0
        self.action = env.process(self.run())
    def run(self):
        while True:
        # sleep for slot time
            yield self.env.timeout(G.SLOT_TIME)
        # Code to determine what happens to a slot and
        # then update node variables accordingly based
        # on the algorithm
class Node_Process(object): 
    def __init__(self, env, id, arrival_rate):
        self.env = env
        self.id = id
        self.arrival_rate = arrival_rate
        # Other state variables
        #self.action = env.process(self.run())
    def run(self):
        # packet arrivals
        print("Arrival Process Started:", self.id)
        # Code to generate the next packet and deal with it
class Packet:
    def __init__(self, identifier, arrival_time):
        self.identifier = identifier
        self.arrival_time = arrival_time
class StatObject(object):
    def __init__(self):
        self.dataset =[]
    def addNumber(self,x):
        self.dataset.append(x)
def main():
    print("Simiulation Analysis of Random Access Protocols")
    random.seed(G.RANDOM_SEED)
    for retran_policy in G.RETRANMISSION_POLICIES:
        for arrival_rate in G.ARRIVAL_RATES:
            env = simpy.Environment()
            slot_stat = StatObject()
            dictionary_of_nodes = {}
            # I chose to pass the list of nodes as a
            # dictionary since I really like python dictionaries :)
            for i in list(range(1,G.N+1)):
                node = Node_Process(env, i, arrival_rate)
                dictionary_of_nodes[i] = node
            server_process = Server_Process(env, dictionary_of_nodes,retran_policy,slot_stat)
            env.run(until=G.SIM_TIME)
# code to determine throughput
# code to plot
#if __name__ == '__main__': main()
main()
