import pandas as pd
from gurobipy import Model, GRB, quicksum
import pandas as pd

def cargar_datos():
    data = {}
    """
    Esta función debe leer los 9 archivos .csv de la instancia y devolver
    un diccionario con todos los parámetros necesarios para construir el modelo.
    """
    nombres_archivos = [
        ("indice", "data/carpeta_salida/Indice asignado a cada planta.csv"),
        ("estrato", "data/carpeta_salida/Estrato de cada planta.csv"),
        ("d_pt", "data/carpeta_salida/d_pt.csv"),
        ("Q_t", "data/carpeta_salida/Q_tv.csv"),
        ("Epsilon_v", "data/carpeta_salida/Epsilon_v.csv"),
        ("L_t", "data/carpeta_salida/L_t.csv"),
        ("B_pt", "data/carpeta_salida/B_pt.csv"),
        ("D_tv", "data/carpeta_salida/D_tv.csv"),
        ("Nabla_r", "data/carpeta_salida/Nabla_r.csv"),
        ("Chi", "data/carpeta_salida/Chi.csv"),
        ("Beta", "data/carpeta_salida/Beta.csv"),
        ("gamma", "data/carpeta_salida/Gamma.csv"),
        ("K_r", "data/carpeta_salida/K_r.csv"),
        ("K_p", "data/carpeta_salida/K_p.csv"),
        ("R_v", "data/carpeta_salida/R_v.csv"),
        ("A_v", "data/carpeta_salida/A_v.csv"),
        ("a_p", "data/carpeta_salida/a_p.csv"),
        ("ζ_τp", "data/carpeta_salida/ζ_τp.csv"),
        ("x_pv0", "data/carpeta_salida/x_pv0.csv"),
        ("e_0vr", "data/carpeta_salida/e_0vr.csv"),
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

        if parametro == "D_tv": #Este no va a ser necesario por como modificamos el modelo
            pass

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

        if parametro == "ζ_τp":
            df = pd.read_csv(ruta)
            data["ζ_τp"] = {}

            for _, fila in df.iterrows():
                planta = int(fila["planta"])
                data["ζ_τp"][planta] = {}
                for tau in range(1, 5):  # Estratos del 1 al 4
                    col = f"si pertenece a estrato {tau}"
                    data["ζ_τp"][planta][tau] = int(fila[col])
        
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