### Importing libraries
import json
from queue import PriorityQueue
import math


### Helper functions
# Another class for priority queue
class PriorityQueue_1:
    def __init__(self):
        self.queue = []

    
    def sort(self):
        self.queue.sort(key= lambda x: x[1])

    def insert(self, key_val, sort=True):
        self.queue.append(key_val)
        if sort:
            self.sort()
    
    def modify(self, key, val):
        for i in self.queue:
            if i[0] == key:
                i[1] = val
                self.sort()
                return
        self.insert([key,val])
    
    def delete(self, key):
        for i in range(len(self.queue)):
            if self.queue[i][0] == key:
                self.queue.pop(i)
                return

    def pop(self, n=0):
        return self.queue.pop(n)

    def isempty(self):
        return len(self.queue) <= 0

### Task 1 - Shortest Path Problem without energy restrictions (shortest distance)


def ucs_search(start, goal, neighbor, dist, cost):
    queue = PriorityQueue()
    #create dictionary
    path = {start: start}
    visited = {}
    distance = {start: 0}
    energyCost = {start: 0}
    # insert the starting index
    queue.put((0, start))
    # while the queue is not empty
    while not queue.empty():
        (currentDist, currentNode) = queue.get()
        if currentNode == goal:
            break
        if (currentNode not in visited):
            visited[currentNode] = 1
            for nextNode in neighbor[currentNode]:
                if nextNode not in visited:
                    nextDist = dist[currentNode + ',' + nextNode]
                    nextCost = cost[currentNode + ',' + nextNode]
                    newDist = nextDist + currentDist
                    newCost = nextCost + energyCost[currentNode]
                    if nextNode in distance:
                        if newDist < distance[nextNode]:
                            queue.put((newDist, nextNode))
                            distance[nextNode] = newDist
                            energyCost[nextNode] = newCost
                            path[nextNode] = path[currentNode] + '->' + nextNode
                    elif nextNode not in distance:
                        distance[nextNode] = newDist
                        queue.put((newDist, nextNode))
                        distance[nextNode] = newDist
                        energyCost[nextNode] = newCost
                        path[nextNode] = path[currentNode] + '->' + nextNode                      
    if goal in path:
        print('Shortest path: ' + path[goal] + '.')
        print("Shortest distance: " + str(distance[goal]) + '.')
        print("Total energy cost: " + str(energyCost[goal]) + '.')
    else:
        print("No shortest path")

def task1():
    with open('G.json') as file:
        neighbor = json.load(file)
    file.close()
    with open('Dist.json') as file2:
        dist = json.load(file2)
    file2.close()
    with open('Cost.json') as file3:
        cost = json.load(file3)
    file3.close()
    start = '1'
    goal = '50'
    ucs_search(start, goal, neighbor, dist, cost)

### Task 2 is after Task 3

### Task 3 - A* Search cost-optimised
# Start node: 1
# End node: 50

# A* search requires both h(n) and g(n)

## Pseudo code
# Have another list to store the path

# Add root node into frontier (priority queue (sorted queue), sorted by f(n))
    # Priority queue will be [("key", f-value), ]
# Take first node and expand it
    # Check if it is the goal
    # Add neighbours into the pq (frontier)
        # Calculate the g(n) value
            # Update the g(n) for that node if it's lower than it is since g(n) is the only variant in calc of f(n)
        # Calculate the f(n) value
            # Update the f(n) only if it is lower than it is currently
        # Keep track of the path via keeping track of parents of each node (if lower g/f value)
        # Add into pq, sorted
    # 

### Evaluating quality of h function
# Max priority queue size
# Number of modifications into the queue
# Number of nodes expanded/popped from the queue

def aStar(graph, cost, dist, coordinates, h1, budget=287932, start= "1", end= "50", weight= 1):

    max_pq = 0
    number_io = 0
    number_nodes = 0


    start = start
    end = end

    # Solution will be stored in parents matrix since storing the path directly is difficult (since expanded node not necessarily in final path)
    # Final solution will trace backwards from target node
    parents = {}
    gvals = {}
    nCosts = {}

    for key in graph.keys():
        parents[key] = "0"
        gvals[key] = math.inf
        nCosts[key] = math.inf

    # Initialise g value of the start
    gvals[start] = 0
    nCosts[start] = 0

    # Priority queue will be here
    pq = PriorityQueue_1()

    # Add start node into frontier
    pq.insert(["1", 0 + weight*h1("1", coordinates)]) # f(), key

    # While priority queue (frontier) is not empty
    while not pq.isempty():
        # Pops the first element, since frontier is sorted by f-value
        v = pq.pop() # v = ["key", f_value]
        number_nodes += 1

        curr = v[0]

        # Expand it
        # Check if it is the goal
        if curr == end:
            break
        # Add children into frontier after calculating f and updating parents
        else:
            for child in graph[curr]:
                # Calculate the g for the child
                # g_val = gvals[curr] + dist[f"{curr},{child}"]
                g_val = gvals[curr] + dist[f"{curr},{child}"]
                n_cost = nCosts[curr] + cost[f"{curr},{child}"]

                # Update the g for the child if needed
                # Since h is the same for the child regardless of path, g is the deciding factor for best path
                # If this is a better than paths before, record it down first
                # modify handles either editing the f value if it's already inside, or adding the child node as a new entry if it's not
                if g_val < gvals[child] and n_cost < budget:
                    parents[child] = curr

                    gvals[child] = g_val
                    nCosts[child] = n_cost

                    h_val = weight*h1(child, coordinates)
                    f_val = g_val + h_val
                    
                    pq.modify(child, f_val)
                    number_io += 1
                    if len(pq.queue) > max_pq:
                        max_pq = len(pq.queue)
        
    # By now either we found an optimal path or not
    # If no path found
    if parents[end] == "0":
        print("No path found")
    else:
        path = []
        curr = end
        # While not root
        while not parents[curr] == "0":
            path.insert(0, curr)
            curr = parents[curr]   
        # Start is the root need to append it
        path.insert(0, start)

        # Calculate the stuff we need
        total_dist = 0
        total_cost = 0
        print("Shortest path: ", end= "")
        for node_index in range(len(path) - 1):
            total_dist += dist[f"{path[node_index]},{path[node_index+1]}"]
            total_cost += cost[f"{path[node_index]},{path[node_index+1]}"]
            print(f"{path[node_index]}->", end="")
        print(path[-1])
        print(f"Shortest distance: {total_dist}")
        print(f"Total energy cost: {total_cost}\n")

        print("A* Search Algorithm specifics:")
        print(f"Weight: {weight}")
        print(f"Total Nodes: {len(graph.keys())}")
        print(f"Expanded nodes: {number_nodes}")
        print(f"Max Size of pq: {max_pq}")
        print(f"Modifications to pq: {number_io}")
        print()

### Heuristic Functions
def h1(n, coordinates, end= "50"):
    """
    Returns the straight-line distance from node to end as h(n), unweighted

    Params:
        n: The node number

        coordinates: The dictionary containing the coordinates of a node
    """
    n_coord = coordinates[n]
    end_coord = coordinates[end]
    # Finds the distance by Pythygoroas theorem C^2 = A^2 + B^2
    straight_line_dist = math.sqrt((n_coord[0] - end_coord[0])**2 + (n_coord[1] - end_coord[1])**2)
    return straight_line_dist


def task3():
    ### Loading the jsons

    # with open is a shortform of opening and closing a file
    # No need to close it as file will automatically close after the end of the block
    # What we're doing is opening the files, while it is open load it into a variable (dictionary), then closing it (auto, since wait open() is used)

    # Coordinates, eg. coordinates["1"]
    with open("Coord.json") as f:
        coordinates = json.load(f)

    # Cost, eg. cost["1,2"], only between two connected nodes
    with open("Cost.json") as f:
        cost = json.load(f)
        
    # Distance, eg. dist["1,2"], only between two connected nodes
    with open("Dist.json") as f:
        dist = json.load(f)

    # Graph, eg. graph["v"] = ["2", "3", "4"]
    with open("G.json") as f:
        graph = json.load(f)

    # Normal aStar
    aStar(graph, cost, dist, coordinates, h1)

    # Weighted, fast but not optimal aStar
    # aStar(graph, cost, dist, coordinates, h1, weight= 1.5)
    # aStar(graph, cost, dist, coordinates, h1, weight= 2)
    # aStar(graph, cost, dist, coordinates, h1, weight= 2.5)
    # aStar(graph, cost, dist, coordinates, h1, weight= 2.75)
    # aStar(graph, cost, dist, coordinates, h1, weight= 3)
    # aStar(graph, cost, dist, coordinates, h1, weight= 8)


### Task 2 - UCS, cost-optimised instead of dist-optimised
# Makes use of the a* Search algorithm where heuristic function is weighted as 0

def task2():
    ### Loading the jsons

    # with open is a shortform of opening and closing a file
    # No need to close it as file will automatically close after the end of the block
    # What we're doing is opening the files, while it is open load it into a variable (dictionary), then closing it (auto, since wait open() is used)

    # Coordinates, eg. coordinates["1"]
    with open("Coord.json") as f:
        coordinates = json.load(f)

    # Cost, eg. cost["1,2"], only between two connected nodes
    with open("Cost.json") as f:
        cost = json.load(f)
        
    # Distance, eg. dist["1,2"], only between two connected nodes
    with open("Dist.json") as f:
        dist = json.load(f)

    # Graph, eg. graph["v"] = ["2", "3", "4"]
    with open("G.json") as f:
        graph = json.load(f)

    # Weight = 0 aStar ie. UCS
    aStar(graph, cost, dist, coordinates, h1, weight=0)


### Execution of functions
print("### Task 1 - UCS (Shortest path/distance) ###")
task1()
print()

print("### Task 2 - UCS (Shortest Path under budget) ###")
task2()
print()

print("### Task 3 - A*Search (Shortest Path under budget) ###")
task3()
print()