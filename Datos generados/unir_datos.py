import pandas as pd
import glob
import os
import shutil
from datetime import datetime

# --- CONFIGURACIÓN ---
direct_base = "C:/Proyectos/Power BI - Logística/Datos generados/"
# Carpeta para mover los archivos procesados y evitar duplicados en la siguiente ejecución
carpeta_procesados = os.path.join(direct_base, "Procesados")

if not os.path.exists(carpeta_procesados):
    os.makedirs(carpeta_procesados)

# Definición de las tablas maestras a actualizar
tablas_maestras = [
    "tabla_ventas",
    "tabla_compras",
    "tabla_stock_inventario",
    "tabla_clientes"
]

def consolidar_archivos():
    for tabla in tablas_maestras:
        archivo_maestro = os.path.join(direct_base, f"{tabla}.csv")
        
        # Buscar archivos que empiecen con el nombre de la tabla y tengan "_add" en alguna parte
        # Ejemplo: tabla_ventas_add.csv, tabla_ventas_add01.csv, etc.
        patron = os.path.join(direct_base, f"{tabla}_add*.csv")
        archivos_incrementales = glob.glob(patron)
        
        if not archivos_incrementales:
            print(f"No se encontraron incrementales para: {tabla}")
            continue

        print(f"Consolidando {len(archivos_incrementales)} archivos en {tabla}.csv...")

        # Lista para almacenar los DataFrames de los archivos encontrados
        lista_dfs = []
        
        for archivo_inc in archivos_incrementales:
            try:
                # Leer el incremental
                df_inc = pd.read_csv(archivo_inc, encoding='utf-8-sig')
                lista_dfs.append(df_inc)
            except Exception as e:
                print(f"Error al leer {archivo_inc}: {e}")

        if lista_dfs:
            # Unir todos los incrementales en uno solo
            df_total_inc = pd.concat(lista_dfs, ignore_index=True)
            
            # Anexar al archivo maestro (mode='a' no escribe el encabezado)
            # Si el archivo maestro no existe, lo crea con encabezado
            file_exists = os.path.isfile(archivo_maestro)
            
            df_total_inc.to_csv(
                archivo_maestro, 
                mode='a', 
                index=False, 
                header=not file_exists, 
                encoding='utf-8-sig'
            )
            
            # MOVER ARCHIVOS PROCESADOS (Para no duplicar datos la próxima vez)
            for archivo_inc in archivos_incrementales:
                nombre_archivo = os.path.basename(archivo_inc)
                # Añadir timestamp al nombre para evitar conflictos si se procesan archivos con el mismo nombre
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nuevo_nombre = f"{timestamp}_{nombre_archivo}"
                shutil.move(archivo_inc, os.path.join(carpeta_procesados, nuevo_nombre))
            
            print(f"Ok: {tabla}.csv actualizado y archivos movidos a /Procesados.")

if __name__ == "__main__":
    consolidar_archivos()