from fucion_imprimir_resultados import imprimir_resultados
from funcion_carga_datos import cargar_datos
from funcion_crear_modelo import construir_modelo
from funcion_resolver_modelo import resolver_modelo

def main():
    data = cargar_datos()
    #for i in data:
    #    print (i, "----->", data[i])
    model = construir_modelo(data)
    resultado = resolver_modelo(model)
    #imprimir_resultados(resultado, data)
if __name__ == "__main__":
    main()