import pandas as pd
import os
import re
import shutil

directorio_base = os.path.dirname(os.path.abspath(__file__))

carpeta_entrada = os.path.join(directorio_base, 'carpeta_entrada')
carpeta_salida = os.path.join(directorio_base, 'carpeta_salida')
archivo_original = os.path.join(carpeta_entrada, 'original.xlsx')

archivo_lista = os.path.join(directorio_base, 'lista_archivos.txt')

os.makedirs(carpeta_salida, exist_ok=True)

# Limpiar carpeta_salida completamente
for nombre in os.listdir(carpeta_salida):
    ruta_completa = os.path.join(carpeta_salida, nombre)
    if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
        os.remove(ruta_completa)
    elif os.path.isdir(ruta_completa):
        shutil.rmtree(ruta_completa)

print(f"[!] Carpeta '{carpeta_salida}' limpiada completamente.")

hojas = pd.read_excel(archivo_original, sheet_name=None)

caracteres_validos = re.compile(r'^[\w\s-]+$')

nombres_archivos = []

# Extraemos solo el nombre de la carpeta para usar en la ruta relativa
carpeta_relativa = os.path.basename(carpeta_salida)

for nombre_hoja, df in hojas.items():
    if caracteres_validos.match(nombre_hoja):
        nombre_archivo_salida = f"{nombre_hoja}.csv"
    else:
        print(f"\n[!] El nombre de la hoja '{nombre_hoja}' contiene caracteres inválidos.")
        print("-> Vista previa del contenido:")
        print(df.head(5))

        while True:
            nuevo_nombre = input(">> Ingresa un nombre válido para guardar esta hoja: ").strip()
            if caracteres_validos.match(nuevo_nombre):
                nombre_archivo_salida = f"{nuevo_nombre}.csv"
                break
            else:
                print("[X] Ese nombre todavía contiene caracteres no permitidos. Intenta nuevamente.")

    ruta_salida = os.path.join(carpeta_salida, nombre_archivo_salida)

    df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    print(f"[OK] Hoja guardada como: {nombre_archivo_salida}")

    nombres_archivos.append((nombre_hoja, f"data/{carpeta_relativa}/{nombre_archivo_salida}"))

with open(archivo_lista, 'w', encoding='utf-8') as f:
    f.write("nombres_archivos = [\n")
    for hoja, archivo in nombres_archivos:
        f.write(f"    (\"{hoja}\", \"{archivo}\"),\n")
    f.write("]\n")

print(f"[OK] Archivo de lista creado/actualizado en: {archivo_lista}")





