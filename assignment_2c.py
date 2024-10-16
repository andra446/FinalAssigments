import networkx as nx

def readInputs(text_file):
    matrix = []

    with open(text_file, 'r') as reader:
        firstline = int(reader.readline().strip())

        for line in reader:
            line = line.rstrip('\n')
            a = line.split()
            a[0] = int(a[0])
            a[1] = int(a[1])
            a[2] = int(a[2])
            a[3] = int(a[3])
            matrix.append(a)

    return matrix, firstline

def calcArcCost(f, c, d):
    cost = f + c * d
    return cost

def createAdjacencyMatrix(iMatrix, nt, nn):
    c_t = []

    for t in range(nt):

        p_t = iMatrix[t][2]
        h_sum = 0
        for i in range(t, nt):
            h_sum += iMatrix[i][3]
        c_t.append(p_t + h_sum)

    d_it = []
    for i in range(nt):
        for t in range(i, nt):
            d_value = 0
            for j in range(i, t + 1):
                d_value += iMatrix[j][0]
            d_it.append(d_value)

    adjacency_matrix = []
    for i in range(nn):
        row = []
        for j in range(nn):
            row.append(0)
        adjacency_matrix.append(row)

    d_it_index = 0
    for t in range(nt):
        f = iMatrix[t][1]
        c = c_t[t]
        for i in range(t, nt):
            d = d_it[d_it_index]
            arcCost = calcArcCost(f, c, d)
            adjacency_matrix[t][i + 1] = arcCost
            d_it_index += 1

    K = 0
    for o in range(numOfTimePeriods):
        h = iMatrix[o][3]
        for m in range(len(d_it)):
            d = d_it[o]

        K += h * d

    return adjacency_matrix, K

def createGraphFromAdjacencyMatrix(adj_matrix):
    G = nx.DiGraph()

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            arc_cost = adj_matrix[i][j]
            if arc_cost != 0:
                G.add_edge(i, j, weight=arc_cost)

    return G

def BellmanFord(Graph, source):
    n = Graph.number_of_nodes()

    distance = list()
    pred = list()

    for i in range(n):
        distance.append(float('inf'))
        pred.append(-1)
    distance[source] = 0

    for _ in range(n - 1):
        for u, v, data in Graph.edges(data=True):
            weight = data.get('weight')
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                pred[v] = u

    for u, v, data in Graph.edges(data=True):
        weight = data.get('weight')
        if distance[u] + weight < distance[v]:
            print('Negative cycle detected')

    return distance, pred

def getShortestPath(pred, target):
    path = []
    current_node = target

    # Walk backwards from target to source
    while current_node != -1:
        path.insert(0, current_node)
        current_node = pred[current_node]
        if current_node == 0:
            path.insert(0, current_node)
            break

    return path

# -------------------------------------------------MAIN CODE START HERE-------------------------------------------------
inputMat, numOfTimePeriods = readInputs("input2b.txt")
numOfNodes = numOfTimePeriods + 1

adjacency_matrix, K = createAdjacencyMatrix(inputMat, numOfTimePeriods, numOfNodes)

G = createGraphFromAdjacencyMatrix(adjacency_matrix)

source_node = 0
target_node = numOfTimePeriods

distances, predecessors = BellmanFord(G, source_node)

shortest_path = getShortestPath(predecessors, target_node)
shortest_distance = distances[target_node]

print("Shortest path from node " + str(source_node) + " to node " + str(target_node) + " is: " + str(shortest_path))
print("Total cost to reach node " + str(target_node) + " is: " + str(shortest_distance))
print("The value of K is: " + str(K))
print("The minimal cost for the lot-sizing problem is: " + str(shortest_distance - K))