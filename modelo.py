import pandas as pd
from gurobipy import Model, GRB, quicksum
import pandas as pd

def construir_modelo(data):
    """
    Esta función debe construir el modelo de optimización utilizando Gurobi
    y los datos provistos en el diccionario `data`.
    """
    model = Model()
    model.setParam("TimeLimit", 60) 

    alpha = model.addVars(data["Areas_Verdes"],data["Estaciones"], vtype = GRB.CONTINUOUS, name = "alpha_vt")
    x = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Plantas"], vtype = GRB.INTEGER, name = "x_vpt")
    y = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Plantas"], vtype = GRB.INTEGER, name = "y_vpt")
    z = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Plantas"], vtype = GRB.INTEGER, name = "z_vpt")
    B = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Riegos"], vtype = GRB.BINARY, name = "B^r_tv")
    e = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Riegos"], vtype = GRB.BINARY, name = "e_tvr")
    w = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Riegos"], vtype = GRB.CONTINUOUS, name = "w_tvr")
    N = model.addVars(data["Estaciones"], data["Areas_Verdes"], vtype = GRB.INTEGER, name = "N_tv")
    s = model.addVars(data["Estaciones"], data["Areas_Verdes"], vtype = GRB.CONTINUOUS, name = "s_tv")
    PI = model.addVars(data["Estaciones"], data["Areas_Verdes"], vtype = GRB.BINARY, name = "pi_tv")
    H = model.addVars(data["Estaciones"], data["Areas_Verdes"], vtype = GRB.CONTINUOUS, name = "H_tv")     # NO ESTA DEFINIDA EN LA NATURELEZA
    q = model.addVars(data["Estaciones"], data["Areas_Verdes"], data["Estratos"], vtype = GRB.BINARY, name = "q_tvtao")    # NO ESTA DEFINIDA EN LA NATURELEZA

    model.update()

    #COMECE A ESCRIBIR LAS RESTRICCIONES DESDE A 6 EN ADELANTE, EN restricciones_De_opti.txt SALE POR QUE NOS LAS CUESTIONARON

    #Seleccion unica de Riego (6)
    model.addConstrs(
        (quicksum(e[t][v][r] for r in data["Riegos"]) == 1
        for t in data["Estaciones"]
        for v in data["Areas_Verdes"]),
        name="R6"
    )
    #Balace de plantas (7) 
    model.addConstrs(
        (x[t-1, v, p] + y[t, v, p] == x[t, v, p] + z[t, v, p]
        for t in data["Estaciones"] if t != min(data["Estaciones"]) #Para partir desde el segundo
        for v in data["Areas_Verdes"]
        for p in data["Plantas"]),
        name="R7"
    )
    #Balance en primer Periodo (8)
    #model.addConstrs(,name = "R8") 
    #
    #model.addConstrs(,name = "R9") 
    #model.addConstrs(,name = "R10") 
    #model.addConstrs(,name = "R11") 
    #model.addConstrs(,name = "R12") 
    #model.addConstrs(,name = "R13") 
    #model.addConstrs(,name = "R14") 
    #model.addConstrs(,name = "R15") 
    #model.addConstrs(,name = "R16") 
    
    #model.addConstrs(((quicksum(data["a_ij"][i][j]*x[i] for i in data["I"]) <= data["b_j"][j] + y[j]) for j in data["J"]), name = "R2")
    #model.addConstrs((w[i] + w[k-1] <= 1 for i in data["I"] for k in data["P_i"][i]), name = "R3")
    #model.addConstr((quicksum(y[j] * data["c_j"][j] for j in data["J"])) <= data["W"], name = "R4")
    #model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    #f_objetivo = quicksum((data["r_i"][i] - data["rho_i"][i]) * x[i] - data["F_i"][i] * w[i] for i in data["I"]) - quicksum(data["c_j"][j] * y[j] for j in data["J"])
    #model.setObjective(f_objetivo, GRB.MAXIMIZE)

    return model