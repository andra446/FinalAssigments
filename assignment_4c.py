import numpy as np
from itertools import product  # for generating all combinations

def readInputs(text_file):
    c = []
    r = []
    b = list()

    with open(text_file, 'r') as reader:
        firstline = reader.readline().strip().split()
        num_m = int(firstline[0])
        num_n = int(firstline[1])

        for _ in range(num_m):
            c_line = reader.readline().rstrip('\n')
            a = c_line.split()
            a[0] = int(a[0])
            a[1] = int(a[1])
            a[2] = int(a[2])
            a[3] = int(a[3])
            a[4] = int(a[4])
            c.append(a)

        for _ in range(num_m):
            r_line = reader.readline().rstrip('\n')
            a = r_line.split()
            a[0] = int(a[0])
            a[1] = int(a[1])
            a[2] = int(a[2])
            a[3] = int(a[3])
            a[4] = int(a[4])
            r.append(a)

        b_line = reader.readline().rstrip('\n')
        a = b_line.split()
        a[0] = int(a[0])
        a[1] = int(a[1])
        a[2] = int(a[2])
        b.extend(a)

    return c, r, b, num_m, num_n


def is_machine_crit(x):
    boolean = False
    x_np = np.array(x)
    column_sums = np.sum(x_np, axis=0)

    if np.any(column_sums == 1):
        boolean = True

    return boolean


def is_capacity_crit(r, x, b):
    boolean = False

    r_np = np.array(r)
    x_np = np.array(x)
    b_np = np.array(b)

    total_usage = np.sum(r_np * x_np, axis=1)

    if np.all(total_usage <= b_np):
        boolean = True

    return boolean

def exhaustive_search(c, r, b, m, n):
    min_cost = float('inf')
    best_x = None
    counter = 1

    # Generate all possible assignments of jobs to machines (n jobs, m machines)
    for iteration in product(range(m), repeat=n):
        x = np.zeros((m, n), dtype=int)

        for j in range(n):
            x[iteration[j], j] = 1

        if is_machine_crit(x) and is_capacity_crit(r, x, b):
            total_cost = calc_cost_of_prod(c, x)

            # Print the current assignment (x_ij matrix) and its total cost
            print("\nIteration " + str(counter) + " of x_ij:")
            for row in x:
                print(row)
            print("Total job allocation cost: " + str(total_cost))

            if total_cost < min_cost:
                iteration_n = counter
                min_cost = total_cost
                best_x = x

            counter += 1

    return best_x, min_cost, iteration_n

def calc_cost_of_prod(c, x):
    c_np = np.array(c)
    total_cost = 0
    num_m, num_n = x.shape

    for j in range(num_n):
        for i in range(num_m):
            if x[i, j] == 1:
                total_cost += c_np[i, j]

    return total_cost

# -------------------------------------------------MAIN CODE START HERE-------------------------------------------------
c_ij, r_ij, b_i, ammount_m, ammount_n = readInputs("input4ex2.txt")

print("The amount of machines are: " + str(ammount_m))
print("The amount of jobs are: " + str(ammount_n))

print("\nThe matrix of c_ij: ")
for row in c_ij:
    print(row)

print("\nThe matrix of r_ij: ")
for row in r_ij:
    print(row)

print("\nb_i: " + str(b_i))

# Perform the exhaustive search for the best job assignment
best_x_ij, minimum_cost, iteration_number= exhaustive_search(c_ij, r_ij, b_i, ammount_m, ammount_n)

if best_x_ij is not None:
    print("\nThe best iteration of x_ij was iteration " + str(iteration_number) + ":")
    for row in best_x_ij:
        print(row)
    print("The minimum total job allocation cost is: " + str(minimum_cost))
else:
    print("No valid assignment found.")
