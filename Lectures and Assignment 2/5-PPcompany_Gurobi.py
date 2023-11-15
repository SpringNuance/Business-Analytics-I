# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 16:38:38 2019

@author: jiliesio
"""

#Import Gurobi solver library
from gurobipy import *

#Data
costs=[[53,95,136,160],
[60,120,132,140],
[210, 190, 89, 71]]

capacities=[10200, 2000, 4100]
demands = [2500, 3000, 5500, 5000]

#Indexes
mills = range(3)
warehouses = range(4)

#Create the LP model in gurobi

model = Model("PP company transportation")

#Decision variables x_ij
x=[]
for i in mills:
    x.append([])
    for j in warehouses:
        x[i].append(model.addVar(lb=0, name="x%d.%d" % (i, j)))
model.update()
    

#Capacity constraints
for i in mills:
    model.addConstr(quicksum(x[i][j] for j in warehouses)<=capacities[i],"Capacity constraint")
model.update() 

#Demand constraints
for j in warehouses:
    model.addConstr(quicksum(x[i][j] for i in mills)==demands[j],"Demand constraint")
model.update() 

#objective function
model.setObjective(quicksum(costs[i][j]*x[i][j] for i in mills for j in warehouses))
model.modelSense = GRB.MINIMIZE
model.update() 

#Find optimal solution       
model.optimize()


#Collect optimal decision variable values to array x_optimal
x_optimal=[]
for i in mills:
    x_optimal.append([])
    for j in warehouses:
        x_optimal[i].append(x[i][j].x)
        
#Print optimal transportation cost and solution
print("Optimal transportation cost:")
print(model.objVal)  
print("Optimal transportation quantities:")
print(x_optimal)     
