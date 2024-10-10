import networkx as nx
import matplotlib.pyplot as plt
import queue

def readInputs(text_file):
    vec = list()

    with open(text_file, 'r') as reader:
        firstline = int(reader.readline().strip())
        for line in reader:
            line = line.rstrip('\n')
            a = line.split()
            a[0] = int(a[0])
            a[1] = int(a[1])
            vec.append(a)

    return vec, firstline

def kahn(G):
    n = G.number_of_nodes()
    nodes = list(G.nodes)
    inDeg = {node: G.in_degree(node) for node in nodes}

    q = queue.Queue()
    for t in nodes:
        if(inDeg[t]) == 0:
            q.put(t)

    errorRef=0
    order = []
    while not q.empty():
        at = q.get()
        order.append(at)

        errorRef += 1

        for s in G.successors(at):
            inDeg[s] -= 1

            if(inDeg[s] == 0):
                q.put(s)

    if errorRef != n:
        return str("Cycles occurs")
    return order

#-------------------------------------------------MAIN CODE START HERE-------------------------------------------------
nodeVec, numOfRowIndexes = readInputs("input1a.txt")

G = nx.DiGraph()
G.add_edges_from(nodeVec)

print("# of rows in the textfile after the first row is: " + str(numOfRowIndexes))
print("The edges are: " + str(nodeVec))
print("The nodeIDs are: " + str(G.nodes))
print("The directed graph with topological ordering: " +  str(kahn(G)))

pos = nx.planar_layout(G)
plt.title("The directed graph with topological ordering:\n" +  str(kahn(G)))
nx.draw(G, pos, with_labels=True, node_size=100, linewidths=10, arrowsize=20)
plt.show()