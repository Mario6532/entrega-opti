import pandas as pd
from gurobipy import GRB

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
