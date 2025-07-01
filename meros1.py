#Siakavara Themistokleia, 4786
import sys
import math

#Entry size = 16bytes + 4bytes = 20 bytes
#max entries per leaf node = floor(node capacity/entry size) = floor(1024/20) = 51
MAX_ENTRIES_PER_LEAF = 51
#Entry size = 32 bytes + 4 bytes = 36 bytes
#max entries per non leaf node = floor(node capacity/entry size) = floor(1024/36)=28
MAX_ENTRIES_PER_NON_LEAF = 28

class Node:
    def __init__(self, nodeID, isLeaf=False):
        self.nodeID = nodeID
        self.isLeaf = isLeaf
        self.entries = []

    def addEntry(self, entry):
        self.entries.append(entry)
    
def calculateMBR(points):
    minX = min(point[1][0] for point in points)
    maxX = max(point[1][0] for point in points)
    minY = min(point[1][1] for point in points)
    maxY = max(point[1][1] for point in points)
    return [minX, minY, maxX, maxY]

def sortByX(point):
    return point[1][0]

def sortByY(point):
    return point[1][1]

def sortByID(point):
    return point[0]

def divideSlices(data, sizeOfData):
    slices = []
    slices = [data[i:i+sizeOfData] for i in range(0, len(data), sizeOfData)]
    return slices

def buildRTree(points, treeArray, currentCounter):
    global treeLevel
    global nodeCounter
    
    if treeLevel == 1:
        maxEntries = MAX_ENTRIES_PER_LEAF
        nodeType = True
    else:
        maxEntries = MAX_ENTRIES_PER_NON_LEAF
        nodeType = False
        
    sortedPoints = sorted(points, key = sortByX)

    #total number of leaf nodes
    N = math.ceil(len(sortedPoints) / maxEntries)
    numSlices = math.ceil(math.sqrt(N))
    #size of each group of rectangles
    M = numSlices * maxEntries

    if numSlices > 1:
        if maxEntries == MAX_ENTRIES_PER_LEAF:
            slices = list(divideSlices(sortedPoints, M))
            sortedSlices = [sorted(item, key = sortByY) for item in slices]
        else:
            sortedSlices = [sorted(sortedPoints, key = sortByID)]
            
        listSlices = [j for i in sortedSlices for j in i]
        
        slices = list(divideSlices(listSlices, maxEntries))

        mbr = [calculateMBR(item) for item in slices]
        
        currentCounter = nodeCounter

        for s in slices:
            newNode = Node(nodeCounter, nodeType)
            for entry in s:
                newNode.addEntry(entry)
            nodeCounter +=1
            treeArray.append(newNode)

        nodeIDs = [i for i in range(currentCounter, nodeCounter)]
 
        treeLevel += 1
        
        newPoints = []
        for a, b in zip(nodeIDs, mbr):
            dataEntry = [a, [b[0], b[1], b[2], b[3]]]
            newPoints.append(dataEntry)
            
        buildRTree(newPoints, treeArray, currentCounter)
    else:
        data = sorted(points, key=sortByY)
        root  = Node(nodeCounter, False)
        for d in data:
            root.addEntry(d)
        treeArray.append(root)
        nodeCounter +=1
    return treeArray

def area(mbr):
    if len(mbr) ==2:
        return 0
    return (mbr[2] - mbr[0])* (mbr[3] - mbr[1])

def printStatistics(nodes):
    print("Height of the tree:", treeLevel)
    level = treeLevel
    nextNodes = []
    totalArea = 0
    
    while level > 0:
        startNode = []
        totalArea = 0
        if nextNodes == []:
            startNode = nodes[-1].entries
        else:
            for n in nextNodes:
                startNode.extend(nodes[n].entries)
        nextNodes = []
        numNodes = 0
        for entry in startNode:
            numNodes += 1
            nextNodes.append(entry[0])

            mbr = entry[1]
            areaMBR = area(mbr)
            totalArea += areaMBR
        print ("Number of nodes at level", level, " is:", numNodes)
        
        if numNodes > 0:
            avgArea = totalArea / numNodes
        else:
            avgArea = 0
        print("Average area of MBRs at level", level, " is:", avgArea)
        level -=1  

def writeFile(nodes, filename):
    with open(filename, 'w') as file:
        file.write(str(nodes[-1].nodeID) + "\n")
        for node in nodes:
            entries = []
            for entry in node.entries:
                entries.append((entry[0], entry[1]))
            if node.isLeaf:
                file.write(f"{node.nodeID}, {len(entries)}, {0 if node.isLeaf else 1}, ")
                formatted_entries = [f"({ptr},({geo[0]},{geo[1]}))" for ptr, geo in entries]
                file.write(', '.join(formatted_entries) + "\n")
                #file.write("\n")
            else:
                file.write(f"{node.nodeID}, {len(entries)}, {0 if node.isLeaf else 1}, ")
                formatted_entries = [f"({ptr},[{geo[0]},{geo[1]},{geo[2]},{geo[3]}])" for ptr, geo in entries]
                file.write(', '.join(formatted_entries) + "\n")
                #file.write("\n")

            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python program.py output_filename")
        sys.exit(1)
    inputFile = "Beijing_restaurants.txt"
    outputFile = sys.argv[1]
    
    with open(inputFile, 'r') as file:
        numPoints = int(file.readline())
        points = [tuple(map(float, line.split())) for line in file]
        points = enumerate(points, start=1)

        nodeCounter = 0
        treeLevel = 1
        nodes = buildRTree(points, [], 0)
        printStatistics(nodes)
        writeFile(nodes, outputFile)
