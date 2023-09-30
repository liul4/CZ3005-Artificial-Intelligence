import json
from queue import PriorityQueue

def main():
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

main()