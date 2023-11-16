# Press shift+enter to run code in a cell

# Import PuLP library; if there is an error message type "pip install pulp" + shift-enter
from pulp import *

#Indices
mills = list(range(3))
warehouses =  list(range(4))

#Parameters
costs=[[53,95,136,160],
[60,120,132,140],
[210, 190, 89, 71]]
capacities=[10200, 2000, 4100]
demands = [2500, 3000, 5500, 5000]

#Create a optimization model (minimization)
model = LpProblem("PP_model", LpMinimize) 

#Create decision variables x_ij
x=[[LpVariable("x_"+str(i+1)+str(j+1),0,None) for j in warehouses] for i in mills] 

#Add objective function:
model += (lpSum([costs[i][j]*x[i][j] for i in mills for j in warehouses]) , "Transportation_costs")

#Add capacity constraints at the mills:
for i in mills: 
    model += (lpSum([x[i][j] for j in warehouses])<=capacities[i], "Capacity_at_mill_"+str(i+1))

#Add balance constraints at the warehouses:
for j in warehouses: 
    model += (lpSum([x[i][j] for i in mills])==demands[j], "Demand_at_warehouse_"+str(j+1))

model.solve() #Solve the optimal solution to model

#Print optimal objective function value:
print("Optimal transportation cost "+str(model.objective.value())+" .")
   
                     
#Print optimal decision variable values: 
for i in mills:
    print("------")
    for j in warehouses:
        if (x[i][j].varValue>0):
            print("Transport "+str(x[i][j].varValue)+" tons from mill "+str(i+1)+" to warehouse "+str(j+1)+".") 
