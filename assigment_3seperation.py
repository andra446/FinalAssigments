from gurobipy import *

w = [5, 6, 8, 6, 4, 6, 5]
v = [6, 4, 6, 7, 5, 8, 8]
x = [1, 0, 0, 1/6, 1, 1, 1]
C = 21

N = len(w)

knapsack_model = Model('knapsack')

z = knapsack_model.addVars(N, vtype=GRB.BINARY, name="z")

obj_fn = sum((1-x[i])*z[i] for i in range(N))
knapsack_model.setObjective(obj_fn, GRB.MINIMIZE)

knapsack_model.addConstr(sum(w[i] * z[i] for i in range(N)) >= C)

knapsack_model.setParam('OutputFlag', False)

knapsack_model.optimize()

print("Objective Function Value: " + str(knapsack_model.objVal))
for v in knapsack_model.getVars():
    print(str(v.varName) + ": " + str(v.x))
