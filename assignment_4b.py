import numpy as np

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

    print("\nResource usage per machine:", total_usage)

    return boolean


def create_x_ij(r, m, n, b):
    r_np = np.array(r)
    b_np = np.array(b)

    x_np = np.zeros((m, n), dtype=int)
    machine_usage = np.zeros(m)

    for col_index in range(n):
        column = np.argsort(r_np[:, col_index])
        for row_index in column:
            updated_machine_usage = machine_usage[row_index] + r_np[row_index, col_index]
            if updated_machine_usage <= b_np[row_index]:
                x_np[row_index, col_index] = 1
                machine_usage[row_index] += r_np[row_index, col_index]
                break

    if is_machine_crit(x_np) and is_capacity_crit(r, x_np, b):
        return x_np
    else:
        return None

def calc_cost_of_prod(c,x):
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

x_ij = create_x_ij(r_ij, ammount_m, ammount_n, b_i)
if x_ij is not None:
    print("\nThe matrix of x_ij: ")
    for row in x_ij:
        print(row)
else:
    print("No valid matrix found.")

totalCost = calc_cost_of_prod(c_ij,x_ij)
print("\nThe total job allocation cost will be: " + str(totalCost))
