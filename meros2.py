#Siakavara Themistokleia, 4786
import sys
import math
import heapq

class Node:
    def __init__(self, nodeID, isLeaf=False):
        self.nodeID = nodeID
        self.isLeaf = isLeaf
        self.entries = []

    def addEntry(self, entry):
        self.entries.append(entry)


def mindist(q, mbr):
    if len(mbr) ==2:
        return math.sqrt(sum((x1-x2)**2 for x1, x2 in zip(q, mbr)))
    qx, qy = q
    minX, minY, maxX, maxY = mbr
    
    if qx < minX:
        xDistance = minX - qx
    elif qx > maxX:
        xDistance = qx - maxX
    else:
        xDistance = 0

    if qy < minY:
        yDistance = minY - qy
    elif qy > maxY:
        yDistance = qy - maxY
    else:
        yDistance = 0

    return math.sqrt(xDistance**2 + yDistance**2)

def knnSearch(nodes, q, k):
    priorityQueue = []
    for entry in nodes[-1].entries:
        initial = mindist(q, entry[1])
        heapq.heappush(priorityQueue, (initial, entry[0]))

    visited = set()
    nearestNeighbors = []
    
    while priorityQueue:
        distance, nodeID = heapq.nsmallest(1,priorityQueue)[0]
        heapq.heappop(priorityQueue)

        checkMin = []
        
        if nodeID in visited:
            continue
        visited.add(nodeID)

        node = nodes[nodeID]
        if node.isLeaf:
            for entry in node.entries:
                heapq.heappush(nearestNeighbors, (mindist(q,entry[1]), entry[0]))
        else:
            for entry in node.entries:
                heapq.heappush(priorityQueue, (mindist(q, entry[1]), entry[0]))
                #print(entry)
        if len(nearestNeighbors) >= k+2:
            nearestN = heapq.nsmallest(k+2,nearestNeighbors)
            for n in priorityQueue:
                heapq.heappush(checkMin, n)
            for n in nearestN:
                heapq.heappush(checkMin, n)
            trueMin = heapq.nsmallest(k+2, checkMin)
            if trueMin != nearestN:
                continue
            break
    return nearestN

def loadRTree(treeFile):
    nodes = []
    with open(treeFile, "r") as f:
        rootID = int(f.readline().strip())
        for line in f:
            data = line.strip().split(", ")
            nodeID = int(data[0])
            isLeaf = not bool(int(data[2]))
            newNode = Node(nodeID, isLeaf)
            for entry in data[3:]:
                if isLeaf:
                    entryData = entry.strip("()").split(",", 1)
                    recordID = int(entryData[0])
                    point = entryData[1].strip("()")
                    data = tuple(map(float, point.split(",")))
                else:
                    entryData = entry.strip("()").split(",", 1)
                    recordID = int(entryData[0])
                    mbr = entryData[1].strip("[]")
                    data = list(map(float, mbr.split(",")))
                newNode.addEntry((recordID, data))
            nodes.append(newNode)
    return nodes

def printNeighbors(neighbors):
    for n in neighbors:
        print(f"({n[1]}, {n[0]})")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python program.py <tree_file> <q_x> <q_y> <k>")
        sys.exit(1)

    treeFile = sys.argv[1]
    q = (float(sys.argv[2]), float(sys.argv[3]))
    k = int(sys.argv[4])

    nodes = loadRTree(treeFile)
    
    nearestNeighbors = knnSearch(nodes, q, k)
    print("The", k+2, "Nearest Neighbors are: ")
    printNeighbors(nearestNeighbors)
    
