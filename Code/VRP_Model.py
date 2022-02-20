import random
import math


class Model:

    # instance variables
    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix_distance = []
        self.matrix_time = []
        self.capacity = -1
        self.trucks = []


    def BuildModel(self):
        random.seed(1)
        depot = Node(0, 0, 50, 50, 0)
        self.allNodes.append(depot)
        totalCustomers = 100
        numberOfTrucks = 30

        for i in range(0, totalCustomers):
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            id = i + 1
            dem = random.randint(1, 5) * 100
            st = 0.25 * 60
            cust = Node(id, st, xx, yy, dem)
            self.allNodes.append(cust)
            self.customers.append(cust)

        rows = len(self.allNodes)
        self.matrix_distance = [[0.0 for xx in range(rows)] for yy in range(rows)]
        self.matrix_time = [[0.0 for xx in range(rows)] for yy in range(rows)]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.xx - b.xx, 2) + math.pow(a.yy - b.yy, 2))
                self.matrix_distance[i][j] = dist
                self.matrix_time[i][j] = (dist / 35) * 60 + self.matrix_time[i][j]

        for i in range(0, numberOfTrucks):
            if (i % 2) == 0:
                truck = Truck(i + 1, 1500)
            else:
                truck = Truck(i + 1, 1200)
            self.trucks.append(Route(depot, st, truck))


class Node:
    def __init__(self, idd, st, xx, yy, dem):
        self.xx = xx
        self.yy = yy
        self.ID = idd
        self.service_time = st
        self.demand = dem
        self.isRouted = False


class Truck:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight


class Route:
    def __init__(self, dp, timecap, truck):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
#        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.truck = truck
#        self.capacity = 0
        self.timecap = timecap
        self.load = 0
        self.timeload = 0
