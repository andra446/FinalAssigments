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


# -------------------------------------------------MAIN CODE START HERE-------------------------------------------------
inputMat, numOfTimePeriods = readInputs("input2b.txt")
numOfNodes = numOfTimePeriods + 1

print("\nThe input matrix is: ")
for row in inputMat:
    print(row)

print("\nThe number of time periods is: " + str(numOfTimePeriods))
print("The number of nodes is: " + str(numOfNodes))

c_t = []
for t in range(numOfTimePeriods):
    p_t = inputMat[t][2]

    h_sum = 0
    for i in range(t, numOfTimePeriods):
        h_sum += inputMat[i][3]

    c_t.append(p_t + h_sum)

d_it = []
for i in range(numOfTimePeriods):
    for t in range(i, numOfTimePeriods):

        d_value = 0
        for j in range(i, t + 1):
            d_value += inputMat[j][0]

        d_it.append(d_value)

print("c_t vector: " + str(c_t))
print("d_it vector: " + str(d_it))

adjacency_matrix = []
for i in range(numOfNodes):
    row = []
    for j in range(numOfNodes):
        row.append(0)
    adjacency_matrix.append(row)

d_it_index = 0
for t in range(numOfTimePeriods):
    f = inputMat[t][1]
    c = c_t[t]

    for i in range(t, numOfTimePeriods):
        d = d_it[d_it_index]

        arcCost = calcArcCost(f, c, d)
        adjacency_matrix[t][i + 1] = arcCost
        d_it_index += 1

# Print the adjacency matrix
print("\nAdjacency Matrix:")
for row in adjacency_matrix:
    print(row)
