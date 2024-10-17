from gurobipy import *

w = [5,6,8,6,4,6,5]
v = [6,4,6,7,5,8,8]
z = [1,0,0,1,1,1,1]
C = 21
N = len(w)

knapsack_model = Model('knapsack')

x = knapsack_model.addVars(N, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="x")

obj_fn = sum(v[i]*x[i] for i in range(N))
knapsack_model.setObjective(obj_fn, GRB.MAXIMIZE)

knapsack_model.addConstr(sum(w[i]*x[i] for i in range(N)) <= C, name="capacity")
knapsack_model.addConstr(sum(z[i]*x[i] for i in range(N)) <= sum(z[i] for i in range(N))-1, name="sep_con")

knapsack_model.setParam('OutputFlag', False)

knapsack_model.optimize()

print("Objective Function Value: " + str(knapsack_model.objVal))
for v in knapsack_model.getVars():
    print(str(v.varName) + ": " + str(v.x))
