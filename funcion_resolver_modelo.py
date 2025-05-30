import pandas as pd
from gurobipy import Model, GRB, quicksum
import pandas as pd

def resolver_modelo(model):
    print ("\n AHORA COMIENZA A RESOLVER EL MODELO\n")
    """
    Esta función debe llamar al solver de Gurobi para resolver el modelo.
    """
    model.optimize()
    return model