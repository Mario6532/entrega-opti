import pandas as pd
from gurobipy import Model, GRB, quicksum
import pandas as pd

def resolver_modelo(model):
    """
    Esta función debe llamar al solver de Gurobi para resolver el modelo.
    """
    model.optimize()
    return model