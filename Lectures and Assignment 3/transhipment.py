# Press shift+enter to run code in a cell

# Import PuLP library; if there is an error message type "pip install pulp" + shift-enter
from pulp import *

#Indices
Mills = list(range(3))
Warehouses =  list(range(4))
Customer_areas = list(range(13))

#Parameters
Prod_max=[9900, 2100, 4200] #Production capacities
Prod_extra = [1100,1400,1500] #Extra capacities
Demand = [650,260,650,130,780,2500,910,3120,910,3640,1040,1650,1780] #Customer area demands
Transp_cost_1 = [[53, 95, 136, 160],
            [60, 120, 132, 140],
            [210, 190, 89, 71]] #Transportation costs from mills to warehouses
Transp_cost_2 = [[100, 120, 150, 160, 300, 310, 340, 490, 430,360, 280, 350, 200],
            [200, 240, 280, 310, 280, 400, 440, 410, 380, 190, 80, 150, 90],
            [280, 260, 320, 400, 140, 319, 290, 240, 230, 80, 60, 60, 160],
            [320, 280, 200, 130, 130, 70, 100, 90, 100, 190, 370, 320, 390]] #Transportation costs from warehouses to customers
Extra_cost = [300000,400000,450000] #Extra capacity costs

model = LpProblem("PP_MILP_model", LpMinimize) #Create a optimization model (minimization)
X=[[LpVariable("x_"+str(i)+str(k),0,None) for k in Warehouses] for i in Mills] #Create decision variables x_ik
Y=[[LpVariable("y_"+str(k)+str(j),0,None) for j in Customer_areas] for k in Warehouses] #Create decision variables y_kj
Z=[LpVariable("z_"+str(i),cat="Binary") for i in Mills ] #Create decision variables z_i

#Set a temporary objective function for testing purposes
model += (lpSum([1*X[i][k] for i in Mills for k in Warehouses]) + lpSum([1*Y[k][j] for k in Warehouses for j in Customer_areas]) + lpSum([1*Z[i] for i in Mills]), "Testing_objective_function")



#TODO: add objective function and constraints here after back from Alps!:

model.solve() #Solve the optimal solution to model

#Print optimal objective function value:
print("Optimal total cost "+str(model.objective.value())+" .")
   
                     
#Print optimal decision variable values: 
for i in Mills:
    print("------")
    if (Z[i].varValue==1):
        print("Purchase extra capacity for mill "+str(i)) 
    for k in Warehouses:
        if (X[i][k].varValue>0):
            print("Transport "+str(X[i][k].varValue)+" tons from mill "+str(i)+" to warehouse "+str(k)+".") 
    

print("---------------")
for k in Warehouses:
    for j in Customer_areas: 
        if (Y[k][j].varValue>0):
            print("Transport "+str(Y[k][j].varValue)+" tons from warehouse "+str(k)+" to customer area "+str(j)+".") 
    print("---")
    
