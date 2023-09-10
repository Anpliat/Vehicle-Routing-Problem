# Vehicle-Routing-Problem (VRP)

<div style="text-align: justify">

### Concept
A company's central warehouse receives numerous orders from 100 customers. The company's trucks are housed in the central warehouse. The purpose is to generate a route for each vehicle with the aim of serving all customers. The construction of the route is subject to certain constraints. 

Each route is an open route, which starts from the main warehouse and visits the various customers. The route is terminated at the last customer visited by the vehicle. Each order must be satisfied by one and only one visit of a vehicle, without order splitting. Moreover, because each truck has a specific product capacity, the truck goods transported must not exceed the truck's maximum capacity. The vehicles travel at 35 km/h, and the goods are unpacked in 15 minutes. The 30 trucks housed in the warehouse are divided into the following categories:

* 15 trucks with a maximum capacity of 1500 kg
* 15 trucks with a maximum capacity of 1200 kg



</div>

### Aim of VRP
Generate a set of routes, one route for every truck, according to the following constraints:
* The total route cost of all routes is minimized.
* Each customer is served once by exactly one truck without order splitting.
* The total demand of the customers visited by a route does not exceed the capacity of the truck.
* Each route is an open route in which trucks leave the depot and serve the customers without returning to the depot.
* The time required to unpack all the products to each customer is 15 minutes.
* The total time duration limit of each route is 3.5 hours that corresponds to 210 minutes by multiplying with 60.


### Methodology
🠊 Use Nearest Neighbor algorithm to construct initial routes

🠊 Design Local Search Algorithm (Operator: Relocation)

🠊 Design VND algorithm (Operators: Relocation, Swap Move and Two-opt)


**Objective Function:** Minimization of the Total Route Cost

### Model Structure

Classes created to initialize the model variables:

:arrow_right: **Model class**
Variable | Content
--- | ---
allNodes | The list with all nodes-customers and depot included.
customers | The list with all nodes-customers without the depot included.
matrix_distance | The list of lists of all distances among the customers included into the distance matrix.
matrix_time | The list of lists of all the times required by tucks to visit each customer - time matrix.
capacity | Model initial capacity.
trucks | The list of 30 trucks which include the 30 routes corresponding to each truck.

*Note: Inside the model class a build-model function is defined which creates the two matrices, the distance matrix calculating all the Euclidean distances among the customers and time matrix which converts the respective distance values to time values dividing by 35 and multiplying by 60.*

:arrow_right: **Node class**
Variable | Content
--- | ---
(x, y) | The exact location of each Node-Customer.
ID | The identity of the customer.
St | The service time needed per customer.
Dem | The product demand of each customer.
IsRouted | First initialization of the unvisited customer (False).

:arrow_right: **Truck class**
Variable | Content
--- | ---
ID | The identity of the truck.
Weight | The trucks’ weight.

:arrow_right: **Route class**
Variable | Content
--- | ---
sequenceOfNodes | The list of routes that include all the customers visited in order started from the depot.
cost | Route cost.
truck | The list of trucks which include all the route and truck features.
load | Total load of the route. 
timeload | Total time of the route.
