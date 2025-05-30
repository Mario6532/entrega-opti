import pandas as pd
from gurobipy import Model, GRB, quicksum
def cargar_datos():


    data = {}
    nombres_archivos = [
        ("d_pt", "d_pt.csv"),
        ("Q_tv" , "q_tv.csv"),
        ("e_v", "epsilon_v.csv"),
        ("L_vt", "L_t.csv"),
        ("B^y_tp", "v_t.csv"),             #cambiar nombre pq hay una variable igual 
        ("D^h_tv", ""),
        ("N_r", ""),
        ("X", ""),
        ("Beta", ""),
        ("gamma",""),
        ("K^r_tv",""),
        ("K^y_tvp", ""),
        ("K^z_tvp", ""),
        ("R_v",""),
        ("A_v",""),
        ("a_p", ""),
        ("chi_tp", "")
    ]
    ###editar cuando tengamos los archivs 
    for combinacion in nombres_archivos:
        parametro = combinacion[0]
        nombre_archivo = combinacion[1]
        archivo = open(nombre_archivo, "r")
        lista = []
        for linea in archivo.readlines():
            linea = linea.replace('"', "").strip("\n")
            if nombre_archivo in ("material_requerido.csv",
"productos_prohibidos.csv"):
                if linea != "":
                    linea = linea.split(",")
                    for i in range(len(linea)):
                        linea[i] = int(linea[i])
                if nombre_archivo == "productos_prohibidos.csv":
                    linea = set(linea)
                lista.append(linea)
            elif nombre_archivo != "productos_prohibidos.csv":
                lista.append(int(linea))
        if parametro in ("W", "N"):
            lista = lista[0]
        data[parametro] = lista
        archivo.close()
    data["M"] = 1000000
    data["I"] = range(len(data["F_i"]))
    data["J"] = range(len(data["c_j"]))
    return data
    #raise NotImplementedError("Implementa esta función para cargar los datos.")
    #####revisar cuando se tengan los archivos 
    ## COSAS QUE PONER EN DATA: V, T, R, P y Tau
def construir_modelo(data):
    """
    Esta función debe construir el modelo de optimización utilizando Gurobi
    y los datos provistos en el diccionario `data`.
    """
    model = Model()
    model.setParam("TimeLimit", 60)
    alpha = model.addVars(data["T"],data["V"], vtype = GRB.CONTINUOUS, name = "alpha_vt")
    x = model.addVars(data["T"], data["V"], data["P"], vtype = GRB.INTEGER, name = "x_tvp")
    y = model.addVars(data["T"], data["V"], data["P"], vtype = GRB.INTEGER, name = "y_tvp")
    z = model.addVars(data["T"], data["V"], data["P"], vtype = GRB.INTEGER, name = "z_tvp")
    B = model.addVars(data["T"], data["V"], data["R"], vtype = GRB.BINARY, name = "B^r_tv")
    e = model.addVars(data["T"], data["V"], data["R"], vtype = GRB.BINARY, name = "e_tvr")
    w = model.addVars(data["T"], data["V"], data["R"], vtype = GRB.CONTINUOUS, name = "w_tvr")
    N = model.addVars(data["T"], data["V"], vtype = GRB.INTEGER, name = "N_tv")
    s = model.addVars(data["T"], data["V"], vtype = GRB.CONTINUOUS, name = "s_tv")
    PI = model.addVars(data["T"], data["V"], vtype = GRB.BINARY, name = "e_tvr")
    H = model.addVars(data["T"], data["V"], vtype = GRB.CONTINUOUS, name = "H_tv")
    ### NO esta definida en la nauraleza
    q = model.addVars(data["T"], data["V"], data["Tau"], vtype = GRB.BINARY, name = "q_tvr")
    ### NO ESTA DEFINIDA EN LA NATURELEZA
    
    ### echo = #
    model.update()
    model.addConstr((data["Epsilon_v"][v] * quicksum(data["Nabla_r"][r] * w[t,v,r] for r in data["R"]) >= quicksum(x[t,v,p] * data["d_pt"][p,t] for p in data["P"]) - data["L_t"][t,v] for v in data["V"] for t in data["T"]), name = "1" )# 

    model.addConstr((w[t,v,r] <= alpha[t,v] for t in data["T"] for v in data["V"] for r in data["R"]), name = "2")# 

    model.addConstr((w[t,v,r] <= data["M"] * e[t,v,r] for t in data["T"] for v in data["V"] for r in data["R"]), name = "3")#

    model.addConstr((w[t,v,r] >= alpha[t,v] - data["M"] * (1-e[t,v,r]) for t in data["T"] for v in data["V"] for r in data["R"]), name = "4")#

    model.addConstr((w[t,v,r] >= 0 for t in data["T"] for v in data["V"] for r in data["R"]), name = "5")#  

    model.addConstr((quicksum(e[t,v,r] for r in data["R"]) == 1 for v in data["V"] for t in data["T"]), name = "6")#

    model.addConstr((x[t-1,v,p] + y[1,v,p] == x[t,v,p] + z[t,v,p] for t in data["T"] for v in data["V"] for p in data["P"]), name = "7")   #

    model.addConstr((x[0,v,p] + y[1,v,p] == x[1,v,p] + z[1,v,p] for v in data["V"] for p in data["P"]), name = "8")#

    model.addConstr((data["Q_t"][t,v] >= quicksum(B[t,v,r] * data["K_r"] * data["A_v"][v] for r in data["R"]) + quicksum(y[t,v,p] * data["K_p"]) for t in data["T"] for v in data["V"]), name = "9") # 

    model.addConstr((quicksum(b[t,v,r] for r in data["R"]) <= 1 for t in data["T"] for v in data["V"]), name = "10")##

    model.addConstr((e[t,v,r] >= b[t,v,r] for t in data["T"] for v in data["V"] for r in data["R"]), name = "11")###

    model.addConstr((e[t,v,r] <= b[t,v,r] + 1- quicksum(b[t, v, r_primo] for r_primo in data["R"] if r_primo != r) for t in data["T"] for r in data["R"] if r_primo != r), name = "12")# listo pero revisar si corre

    model.addConstr((e[t,v,r] <= e[t-1,v,r] + b[t, v, r] for r in data["R"] for t in data["T"] for r in data["R"]), name = "13")# listo pero revisar si corre

    model.addConstr((b[t, v, r] <= 1- e[t-1,v,r] for r in data["R"] for t in data["T"] for r in data["R"] if r_primo != r), name = "14")# listo pero revisar si corre

    model.addConstr((quicksum(e[0,v,r] == 1 for r in data["R"]) for v in data["V"]), name = "15") 

    model.addConstr((y[t,v,p] <= data["M"] * data["B_pt"][t,p] for t in data["T"] for v in data["V"] for p in data["P"]), name = "16") #VOY ACA

    model.addConstr((H[data["T"][-1],v] >= data["D_tv"][data["T"][-1],v] for v in data["V"]), name = "17")#####DUdable

    ####model.addConstr((H[0,v] >= data["D_tv"][0,v] for v in data["V"]), name = "18")#DUDABLE 

    model.addConstr((H[t,v] == data["Chi"] * N[t,v] + data["beta"] * s[t,v] - data["gamma"] * PI[t,v] for v in data["V"] for t in data["T"]), name = "18")#

    model.addConstr((quicksum(y[t,v,p] for P in data["P"]) <= PI[t,v] * data["M"] for v in data["V"] for t in data["T"]), name = "19")#

    model.addConstr((quicksum(y[t,v,p] for P in data["P"]) <= data["B_pt"][t,p] * data["M"] for v in data["V"] for t in data["T"] for p in data["P"]), name = "20")#  DUDABLE 

    model.addConstr((quicksum(z[t,v,p] for P in data["P"]) <= PI[t,v] * data["M"] for v in data["V"] for t in data["T"]), name = "21")#

    model.addConstr((s[t,v] * data["A_v"][v] == quicksum(x[t,v,p] * data["a_p"][p] for p in data["P"]) for t in data["T"] for v in data["V"]), name = "22")#

    model.addConstr((data["A_v"][v] >= quicksum(x[t,v,p] * data["a_p"][p] for p in data["P"]) for t in data["T"] for v in data["V"]), name = "23")#

    model.addConstr((quicksum(x[t,v,p] * data["ζ_τp"][t,p] for p in data["P"]) <=  data["M"] * q[t,v,tau] for t in data["T"] for v in data["V"] for tau in data["Tau"]), name = "24")#

    model.addConstr((quicksum(x[t,v,p] * data["ζ_τp"][t,p] for p in data["P"]) >= q[t,v,tau] for t in data["T"] for v in data["V"] for tau in data["Tau"]), name = "25")#

    model.addConstr((N[t,v] == quicksum(q[t,v,tau] for tau in data["Tau"]) for v in data["V"] for t in data["T"]), name = "26") #


    f_objetivo = quicksum(quicksum(alpha[t,v] for t in data["T"]) for v in data["V"]) ####

    model.setObjective(f_objetivo, GRB.MINIMIZE) #

    return model
 #raise NotImplementedError("Implementa esta función para construir el modelo.")
def resolver_modelo(model):
    """
    Esta función debe llamar al solver de Gurobi para resolver el modelo.
    """
    model.optimize()
    return model
def imprimir_resultados(model, data):
    """
    Esta función debe imprimir de forma clara el valor óptimo (con su unidad)
    y la cantidad de productos producidos de cada tipo.
    """
    print(f"\nValor Optimo: ${model.ObjVal}")
    print(f"\nCantidad producida de cada producto:")
    for i in data["I"]:
        var_w = model.getVarByName(f"w_i[{i}]")
        var_x = model.getVarByName(f"x_i[{i}]")
        #print(var_x)
        if var_w.X > 0.5:
            print(f"-> Producto {i+1}: {var_x.X} unidades")
        else:
            print((f"-> Producto {i+1}: {var_x.X} unidades (No Se Produjo)"))
    return
    #raise NotImplementedError("Implementa esta función para imprimir losresultados.")
def main():
    data = cargar_datos()
    for i in data:
        print (i, "----->", data[i])
    model = construir_modelo(data)
    resultado = resolver_modelo(model)
    imprimir_resultados(resultado, data)
if __name__ == "__main__":
    main()