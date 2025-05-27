import pandas as pd
from gurobipy import Model, GRB, quicksum
def cargar_datos():
    """
     Esta función debe leer los 9 archivos .csv de la instancia y devolver
    un diccionario con todos los parámetros necesarios para construir el modelo.
    """
    data = {}
    nombres_archivos = [
        ("d_pt", "litros_demandados.csv"),
        ("Q_tv" , "ingreso_por_unidad.csv"),
        ("e_v", "material_requerido.csv"),
        ("L_vt", "material_disponible.csv"),
        ("B^y_tp", "costo_material.csv"),
        ("D^h_tv", "costo_variable.csv"),
        ("N_r", "costo_fijo.csv"),
        ("X", "presupuesto_materiales.csv"),
        ("Beta", "maximo_productos.csv"),
        ("Gamma","archivo.csv"),
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
    ## COSAS QUE PONER EN DATA: v, t, r, p
def construir_modelo(data):
    """
    Esta función debe construir el modelo de optimización utilizando Gurobi
    y los datos provistos en el diccionario `data`.
    """
    model = Model()
    model.setParam("TimeLimit", 60)
    a = model.addVars(data["V"],data["T"], vtype = GRB.CONTINUOUS, name = "a_vt")
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
    q = model.addVars(data["T"], data["V"], data["R"], vtype = GRB.BINARY, name = "q_tvr")
    ### NO ESTA DEFINIDA EN LA NATURELEZA
    

    model.update()
    model.addConstrs((x[i] <= data["M"] * w[i] for i in data["I"] ), name = "1" ) 

    model.addConstrs((w[t,v,r] <= a[t,v] for t in data["T"] for v in data["V"] for r in data["R"]), name = "2")#echo 

    model.addConstrs((w[i] + w[k-1] <= 1 for i in data["I"] for k in data["P_i"][i]), name = "3")

    model.addConstr((quicksum(y[j] * data["c_j"][j] for j in data["J"])) <=data["W"], name = "R4")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "6")

    model.addConstr((x[t-1,v,p] + y[1,v,p] == x[t,v,p] + z[t,v,p] for t in data["T"] for v in data["V"] for p in data["P"]), name = "7")   #echo 

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")

    model.addConstr((quicksum(w[i] for i in data["I"]) <= data["N"]), name = "R5")


    f_objetivo = quicksum((data["r_i"][i] - data["rho_i"][i]) * x[i] - data["F_i"][i] * w[i] for i in data["I"]) - quicksum(data["c_j"][j] * y[j] for j in data["J"])

    model.setObjective(f_objetivo, GRB.MAXIMIZE)

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