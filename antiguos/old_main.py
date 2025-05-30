import pandas as pd
from gurobipy import Model, GRB, quicksum
from main import cargar_datos
def cargar_datos_old():


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
    b = model.addVars(data["T"], data["V"], data["R"], vtype = GRB.BINARY, name = "B^r_tv")
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
    [model.addConstr(data["Epsilon_v"][v] * quicksum(data["Nabla_r"][r] * w[t,v,r] for r in data["R"]) >= quicksum(x[t,v,p] * data["d_pt"][p][t] for p in data["P"]) - data["L_t"][t] , name="1") for v in data["V"] for t in data["T"]]

    [model.addConstr((w[t,v,r] <= alpha[t,v]), name = "2") for t in data["T"] for v in data["V"] for r in data["R"]] 

    [model.addConstr((w[t,v,r] <= data["M"] * e[t,v,r]), name = "3") for t in data["T"] for v in data["V"] for r in data["R"]]

    [model.addConstr((w[t,v,r] >= alpha[t,v] - data["M"] * (1-e[t,v,r])), name = "4") for t in data["T"] for v in data["V"] for r in data["R"]]

    [model.addConstr((w[t,v,r] >= 0), name = "5") for t in data["T"] for v in data["V"] for r in data["R"]]

    [model.addConstr((quicksum(e[t,v,r] for r in data["R"]) == 1), name = "6") for v in data["V"] for t in data["T"]]

    [model.addConstr((x[t-1,v,p] + y[1,v,p] == x[t,v,p] + z[t,v,p]), name = "7")for t in data["T"] if t > 1 for v in data["V"] for p in data["P"] ]  #ver en el latex

    [model.addConstr((x[1,v,p] + y[1,v,p] == x[1,v,p] + z[1,v,p]), name = "8") for v in data["V"] for p in data["P"]] #####?????   revisar los 0 y 1 en la x sobre todo 

    [model.addConstr((data["Q_t"][t] >= quicksum(b[t,v,r] * data["K_r"][r] * data["A_v"][v] for r in data["R"]) + quicksum(y[t,v,p] * data["K_p"][p] for p in data["P"])), name = "9") for t in data["T"] for v in data["V"]] # 

    [model.addConstr((quicksum(b[t,v,r] for r in data["R"]) <= 1 ), name = "10")for t in data["T"] for v in data["V"]]##

    [model.addConstr((e[t,v,r] >= b[t,v,r] ), name = "11")for t in data["T"] for v in data["V"] for r in data["R"]]###

    [model.addConstr((e[t,v,r] <= b[t,v,r] + 1- quicksum(b[t, v, r_primo] for r_primo in data["R"] if r_primo != r)), name = "12") for v in data["V"] for t in data["T"] for r in data["R"]]# listo pero revisar si corre

    [model.addConstr((e[t,v,r] <= e[t-1,v,r] + b[t, v, r]), name = "13") for v in data["V"] for t in data["T"] for r in data["R"] if t > 1]# listo pero revisar si corre

    [model.addConstr((b[t, v, r] <= 1- e[t-1,v,r]), name = "14") for r in data["R"] for t in data["T"] for v in data["V"] if t > 1]# listo pero revisar si corre

    [model.addConstr((quicksum(e[1,v,r] for r in data["R"])  == 1), name = "15") for v in data["V"]] 

    [model.addConstr((y[t,v,p] <= data["M"] * data["B_pt"][p][t]), name = "16") for t in data["T"] for v in data["V"] for p in data["P"]]#VOY ACA

    #[model.addConstr((H[max(data["T"]),v] >= data["D_tv"][max(data["T"])][v]), name = "17") for v in data["V"]]#####DUdable

    ####model.addConstr((H[0,v] >= data["D_tv"][0,v] for v in data["V"]), name = "18")#DUDABLE 

    [model.addConstr((H[t,v] == data["Chi"] * N[t,v] + data["Beta"] * s[t,v] - data["gamma"] * PI[t,v]), name = "18") for v in data["V"] for t in data["T"]]#

    [model.addConstr((quicksum(y[t,v,p] for p in data["P"]) <= PI[t,v] * data["M"]), name = "19")for v in data["V"] for t in data["T"]]#

    [model.addConstr((quicksum(y[t,v,p] for p in data["P"]) <= data["B_pt"][p][t] * data["M"] ), name = "20") for v in data["V"] for t in data["T"] for p in data["P"]]#  DUDABLE 

    [model.addConstr((quicksum(z[t,v,p] for p in data["P"]) <= PI[t,v] * data["M"]), name = "21")for v in data["V"] for t in data["T"]]

    [model.addConstr((s[t,v] * data["A_v"][v] == quicksum(x[t,v,p] * data["a_p"][p] for p in data["P"])), name = "22")for t in data["T"] for v in data["V"]]#

    [model.addConstr((data["A_v"][v] >= quicksum(x[t,v,p] * data["a_p"][p] for p in data["P"]) ), name = "23")for t in data["T"] for v in data["V"]]

    [model.addConstr((quicksum(x[t,v,p] * data["ζ_τp"][p][tau] for p in data["P"]) <=  data["M"] * q[t,v,tau]), name = "24")for t in data["T"] for v in data["V"] for tau in data["Tau"]]

    [model.addConstr((quicksum(x[t,v,p] * data["ζ_τp"][p][tau] for p in data["P"]) >= q[t,v,tau] ), name = "25")for t in data["T"] for v in data["V"] for tau in data["Tau"]]

    [model.addConstr((N[t,v] == quicksum(q[t,v,tau] for tau in data["Tau"])), name = "26")for v in data["V"] for t in data["T"]] #


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
    #imprimir_resultados(resultado, data)
if __name__ == "__main__":
    main()