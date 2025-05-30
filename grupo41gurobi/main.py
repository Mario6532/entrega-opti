import pandas as pd
from gurobipy import Model, GRB, quicksum

def cargar_datos():

    data = {}
    """
    Esta función debe leer los 9 archivos .csv de la instancia y devolver
    un diccionario con todos los parámetros necesarios para construir el modelo.
    """
    nombres_archivos = [
        ("indice", "data/Indice asignado a cada planta.csv"),
        ("estrato", "data/Estrato de cada planta.csv"),
        ("d_pt", "data/d_pt.csv"),
        ("Q_t", "data/Q_tv.csv"),
        ("Epsilon_v", "data/Epsilon_v.csv"),
        ("L_t", "data/L_t.csv"),
        ("B_pt", "data/B_pt.csv"),
        ("Nabla_r", "data/Nabla_r.csv"),
        ("Chi", "data/Chi.csv"),
        ("Beta", "data/Beta.csv"),
        ("gamma", "data/Gamma.csv"),
        ("K_r", "data/K_r.csv"),
        ("K_p", "data/K_p.csv"),
        ("R_v", "data/R_v.csv"),
        ("A_v", "data/A_v.csv"),
        ("a_p", "data/a_p.csv"),
        ("dz_tau_p", "data/dz_tau_p.csv"),
        ("x_pv0", "data/x_pv0.csv"),
        ("e_0vr", "data/e_0vr.csv"),
]

    for parametro, ruta in nombres_archivos:
        df = pd.read_csv(ruta)
        
        if parametro == "indice":
            data["nombre_p"] = dict(zip(df["Planta"], df["Nombre Común"]))
            data["P"] = set(df["Planta"].tolist())

        if parametro == "estrato":
            data["estrato_p"] = dict(zip(df["Planta"], df["Estrato"]))
            data["Tau"] = set(df["Estrato"].tolist())

        if parametro == "d_pt":
            data["d_pt"] = {}
            estaciones = set()
            for _, row in df.iterrows():
                planta = int(row["Planta"])
                estacion = int(row["Estación (periodo)"])
                litros = float(row["Litros de agua demandados por planta por estación"])
                estaciones.add(estacion)
                if planta not in data["d_pt"]:
                    data["d_pt"][planta] = {}
                data["d_pt"][planta][estacion] = litros
            data["T"] = estaciones #Estaciones o Periodos

        if parametro == "Q_t":
            data["Q_t"] = dict(zip(df["Estación"], df["Presupuesto (pesos)"]))

        if parametro == "Epsilon_v":
            data["Epsilon_v"] = dict(zip(df["Area Verde"], df["Capacidad de infiltración del suelo"]))
            data["V"] = set(df["Area Verde"].tolist())

        if parametro == "L_t":
            data["L_t"] = dict(zip(df["Estación"], df["Litros de agua aportados por lluvia"]))  

        if parametro == "B_pt":
            data["B_pt"] = {}

            for _, row in df.iterrows():
                planta = int(row["Planta"])
                estacion = int(row["Estación"])
                se_puede_plantar = int(row["¿Se puede plantar?"])

                if planta not in data["B_pt"]:
                    data["B_pt"][planta] = {}

                data["B_pt"][planta][estacion] = se_puede_plantar

        if parametro == "Nabla_r":
            data["Nabla_r"] = dict(zip(df["Tipo  riego"], df["Eficiencia"]))
            data["R"] = set(df["Tipo  riego"].tolist()) 

        if parametro == "Chi":
            df = pd.read_csv(ruta, header=None)
            data["Chi"] = float(df.iloc[1, 0])

        if parametro == "Beta":
            df = pd.read_csv(ruta, header=None)
            data["Beta"] = float(df.iloc[1, 0])

        if parametro == "gamma":
            df = pd.read_csv(ruta, header=None)
            data["gamma"] = float(df.iloc[1, 0])

        if parametro == "K_r":
            data["K_r"] = dict(zip(df["Tipo de Riego"], df["Costo asociado por metro cuadrado"]))

        if parametro == "K_p":
            data["K_p"] = dict(zip(df["Planta"], df["Costo unitario"]))

        if parametro == "R_v":
            data["R_v"] = dict(zip(df["Area verde"], df["Tipo de Riego inicial"]))

        if parametro == "A_v":
            data["A_v"] = dict(zip(df["Area verde"], df["Superficie"]))

        if parametro == "a_p":
            data["a_p"] = dict(zip(df["planta"], df["superficie que cubre en m^2"]))

        if parametro == "dz_tau_p":
            df = pd.read_csv(ruta)
            data["dz_tau_p"] = {}

            for _, fila in df.iterrows():
                planta = int(fila["planta"])
                data["dz_tau_p"][planta] = {}
                for tau in range(1, 5):  # Estratos del 1 al 4
                    col = f"si pertenece a estrato {tau}"
                    data["dz_tau_p"][planta][tau] = int(fila[col])
        
        if parametro == "x_pv0":
            df = pd.read_csv(ruta)
            data["x_pv0"] = {}

            for _, fila in df.iterrows():
                planta = int(fila["Planta"])
                area_verde = int(fila["Area verde"])
                unidades = int(fila["Unidades"])

                if planta not in data["x_pv0"]:
                    data["x_pv0"][planta] = {}
                data["x_pv0"][planta][area_verde] = unidades

        if parametro == "e_0vr":
            df = pd.read_csv(ruta)
            data["e_0vr"] = {}

            for _, fila in df.iterrows():
                area = int(fila["area verde"])
                riego = int(fila["Riegos"])
                valor = int(fila["valor"])

                if area not in data["e_0vr"]:
                    data["e_0vr"][area] = {}

                data["e_0vr"][area][riego] = valor
    
    data["M"] = 10**10

    data["D"] = 1.3

    print ("\n SE CARGAN LOS DATOS\n")

    return data

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
    PI = model.addVars(data["T"], data["V"], vtype = GRB.BINARY, name = "PI_tv")
    H = model.addVars(data["T"], data["V"], vtype = GRB.CONTINUOUS, name = "H_tv")
    q = model.addVars(data["T"], data["V"], data["Tau"], vtype = GRB.BINARY, name = "q_tv_tau")

    model.update()
    [model.addConstr( x[t,v,p] >= 0 , name = "nv1") for t in data["T"] for v in data["V"] for p in data["P"]]
    [model.addConstr( y[t,v,p] >= 0 , name = "nv2") for t in data["T"] for v in data["V"] for p in data["P"]]
    [model.addConstr( z[t,v,p] >= 0 , name = "nv3") for t in data["T"] for v in data["V"] for p in data["P"]]
    [model.addConstr( w[t,v,r] >= 0 , name = "nv4") for t in data["T"] for v in data["V"] for r in data["R"]]
    [model.addConstr( N[t,v] >= 0 , name = "nv1") for t in data["T"] for v in data["V"]]
    [model.addConstr( alpha[t,v] >= 0 , name = "nv1") for t in data["T"] for v in data["V"]]
    [model.addConstr( s[t,v] >= 0 , name = "nv1") for t in data["T"] for v in data["V"]]
    [model.addConstr( H[t,v] >= 0 , name = "nv1") for t in data["T"] for v in data["V"]]
    
    [model.addConstr(data["Epsilon_v"][v] * quicksum(data["Nabla_r"][r] * w[t,v,r] for r in data["R"]) >= quicksum(x[t,v,p] * data["d_pt"][p][t] for p in data["P"]) - data["L_t"][t] , name="1") for v in data["V"] for t in data["T"]]
    
    [model.addConstr((w[t,v,r] <= alpha[t,v]), name = "2") for t in data["T"] for v in data["V"] for r in data["R"]] 

    [model.addConstr((w[t,v,r] <= data["M"] * e[t,v,r]), name = "3") for t in data["T"] for v in data["V"] for r in data["R"]]

    [model.addConstr((w[t,v,r] >= alpha[t,v] - data["M"] * (1-e[t,v,r])), name = "4") for t in data["T"] for v in data["V"] for r in data["R"]]

    [model.addConstr((w[t,v,r] >= 0), name = "5") for t in data["T"] for v in data["V"] for r in data["R"]]

    [model.addConstr((quicksum(e[t,v,r] for r in data["R"]) == 1), name = "6") for v in data["V"] for t in data["T"]]

    [model.addConstr((x[t-1,v,p] + y[t,v,p] == x[t,v,p] + z[t,v,p]), name = "7")for t in data["T"] if t > 1 for v in data["V"] for p in data["P"] ]  #ver en el latex

    [model.addConstr((data["x_pv0"][p][v] + y[1,v,p] == x[1,v,p] + z[1,v,p]), name = "8") for v in data["V"] for p in data["P"]] 

    [model.addConstr((data["Q_t"][t] >= quicksum(b[t,v,r] * data["K_r"][r] * data["A_v"][v] for r in data["R"]) + quicksum(y[t,v,p] * data["K_p"][p] for p in data["P"])), name = "9") for t in data["T"] for v in data["V"]] # 

    [model.addConstr((quicksum(b[t,v,r] for r in data["R"]) <= 1 ), name = "10")for t in data["T"] for v in data["V"]]##

    [model.addConstr((e[t,v,r] >= b[t,v,r] ), name = "11")for t in data["T"] for v in data["V"] for r in data["R"]]###

    [model.addConstr((e[t,v,r] <= b[t,v,r] + 1- quicksum(b[t, v, r_primo] for r_primo in data["R"] if r_primo != r)), name = "12") for v in data["V"] for t in data["T"] for r in data["R"]]# listo pero revisar si corre

    [model.addConstr((e[t,v,r] <= e[t-1,v,r] + b[t, v, r]), name = "13") for v in data["V"] for t in data["T"] for r in data["R"] if t > 1]# listo pero revisar si corre

    [model.addConstr((b[t, v, r] <= 1- e[t-1,v,r]), name = "14") for r in data["R"] for t in data["T"] for v in data["V"] if t > 1]# listo pero revisar si corre

    [model.addConstr((quicksum(data["e_0vr"][v][r] for r in data["R"])  == 1), name = "15") for v in data["V"]]

    [model.addConstr((y[t,v,p] <= data["M"] * data["B_pt"][p][t]), name = "16") for t in data["T"] for v in data["V"] for p in data["P"]]#VOY ACA

    [model.addConstr((H[max(data["T"]),v] >= data["D"]), name = "17") for v in data["V"]]

    [model.addConstr((H[t,v] == data["Chi"] * N[t,v] + data["Beta"] * s[t,v] - data["gamma"] * PI[t,v]), name = "18") for v in data["V"] for t in data["T"]]#

    [model.addConstr((quicksum(y[t,v,p] for p in data["P"]) <= PI[t,v] * data["M"]), name = "19")for v in data["V"] for t in data["T"]]#

    [model.addConstr((quicksum(y[t,v,p] for p in data["P"]) <= data["B_pt"][p][t] * data["M"] ), name = "20") for v in data["V"] for t in data["T"] for p in data["P"]]#  DUDABLE 

    [model.addConstr((quicksum(z[t,v,p] for p in data["P"]) <= PI[t,v] * data["M"]), name = "21")for v in data["V"] for t in data["T"]]

    [model.addConstr((s[t,v] * data["A_v"][v] == quicksum(x[t,v,p] * data["a_p"][p] for p in data["P"])), name = "22")for t in data["T"] for v in data["V"]]#

    [model.addConstr((data["A_v"][v] >= quicksum(x[t,v,p] * data["a_p"][p] for p in data["P"]) ), name = "23")for t in data["T"] for v in data["V"]]

    [model.addConstr((quicksum(x[t,v,p] * data["dz_tau_p"][p][tau] for p in data["P"]) <=  data["M"] * q[t,v,tau]), name = "24")for t in data["T"] for v in data["V"] for tau in data["Tau"]]

    [model.addConstr((quicksum(x[t,v,p] * data["dz_tau_p"][p][tau] for p in data["P"]) >= q[t,v,tau] ), name = "25")for t in data["T"] for v in data["V"] for tau in data["Tau"]]

    [model.addConstr((N[t,v] == quicksum(q[t,v,tau] for tau in data["Tau"])), name = "26")for v in data["V"] for t in data["T"]] #

    f_objetivo = quicksum(quicksum(alpha[t,v] for t in data["T"]) for v in data["V"]) ####

    model.setObjective(f_objetivo, GRB.MINIMIZE) #

    print ("\n SE CREA EL MODELO\n")

    return model

def resolver_modelo(model):

    print ("\n AHORA COMIENZA A RESOLVER EL MODELO\n")
    """
    Esta función debe llamar al solver de Gurobi para resolver el modelo.
    """
    model.optimize()
    return model

def imprimir_resultados(model, data, output_filename_base="resultados"):
    """
    Guarda dos archivos CSV:
    - Todas las variables del modelo.
    - Un resumen por plaza y planta: total sacadas, plantadas y saldo final.
    """
    if model.status == GRB.OPTIMAL:
        # 1. Guardar todas las variables del modelo
        all_vars = [[var.varName, var.X] for var in model.getVars()]
        df_all_vars = pd.DataFrame(all_vars, columns=["Variable", "Valor"])
        df_all_vars.to_csv(f"{output_filename_base}_variables.csv", index=False, sep=';', decimal='.')

    else:
        print(f"Modelo no óptimo. Estado: {model.status}")

def main():
    data = cargar_datos() 
    model = construir_modelo(data) 
    resultado_modelo = resolver_modelo(model) 
    imprimir_resultados(resultado_modelo, data) 

if __name__ == "__main__":
    main()