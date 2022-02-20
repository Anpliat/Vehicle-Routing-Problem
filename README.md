# Vehicle-Routing-Problem (VRP)

### Business Scenario
A company's central warehouse receives numerous orders from 100 customers. The company's trucks are housed in the central warehouse. The purpose is to generate a route for each vehicle with the aim of serving all customers. The construction of the route is subject to certain constraints. 

Each route is an open route, which starts from the main warehouse and visits the various customers. The route is terminated at the last customer visited by the vehicle. Each order must be satisfied by one and only one visit of a vehicle, without order splitting. Moreover, because each truck has a specific product capacity, the truck goods transported must not exceed the truck's maximum capacity. The vehicles travel at 35 km/h, and the goods are unpacked in 15 minutes. The 30 trucks housed in the warehouse are divided into the following categories:

* 15 trucks with a maximum capacity of 1500 kg
* 15 trucks with a maximum capacity of 1200 kg

### Aim of VRP
Generate a set of routes, one route for every truck according to the following constraints:
* The total route cost of all routes is minimized.
* Each customer is served once by exactly one truck without order splitting.
* The total demand of the customers visited by a route does not exceed the capacity of the truck.
* Each route is an open route in which trucks leave the depot and serve the customers without returning to the depot.
* The time required to unpack all the products to each customer is 15 minutes.
* The total time duration limit of each route is 3.5 hours that corresponds to 210 minutes by multiplying with 60.

