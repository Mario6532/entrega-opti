# main_definitivo.py
from fucion_imprimir_resultados import imprimir_resultados
from funcion_carga_datos import cargar_datos #
from funcion_crear_modelo import construir_modelo #
from funcion_resolver_modelo import resolver_modelo #

def main():
    data = cargar_datos() #
    for i in data:
         print (i, "----->", data[i])
    model = construir_modelo(data) #
    resultado_modelo = resolver_modelo(model) # # 'resultado' es el modelo ya resuelto

    # Descomenta y usa la siguiente línea:
    imprimir_resultados(resultado_modelo, data) #
    # Opcionalmente, puedes especificar un nombre base para los archivos de salida:
    # imprimir_resultados(resultado_modelo, data, output_filename_base="mi_salida_personalizada")

if __name__ == "__main__":
    main()