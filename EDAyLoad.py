import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import sqlalchemy as sa

# --- CONFIGURACIÓN ---
direct_base = "C:/Proyectos/Power BI - Logística/Datos generados/"
direct_graficos = os.path.join(direct_base, "Graficos_Segmentados")
if not os.path.exists(direct_graficos): os.makedirs(direct_graficos)

# Lista de productos según tu catálogo de Surcomotor
VEHICULOS = ["AUTOS", "CAMIONETAS"]

def categorizar_producto(nombre_prod):
    """Clasifica el producto para normalizar las escalas del EDA"""
    nombre_upper = str(nombre_prod).upper()
    if any(v in nombre_upper for v in VEHICULOS):
        return "Vehículo"
    return "Repuesto"

def generar_eda_segmentado(df, nombre_tabla):
    print(f"Analizando {nombre_tabla} por segmentos...")
    sns.set_theme(style="white")
    
    # Aseguramos que exista la columna de categoría
    if 'Producto' in df.columns:
        df['Categoria'] = df['Producto'].apply(categorizar_producto)
    else:
        df['Categoria'] = "General"

    cols_analisis = [c for c in ['Precio_V', 'Precio_C', 'Cant', 'Monto'] if c in df.columns]

    for col in cols_analisis:
        # 1. Boxplot Comparativo: Vehículos vs Repuestos
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Categoria', y=col, data=df, hue='Categoria', palette="Set1", legend=False)
        plt.title(f"Comparativa de {col}: Vehículos vs Repuestos")
        plt.yscale('log') # Escala logarítmica para ver ambos mundos claramente
        plt.savefig(os.path.join(direct_graficos, f"{nombre_tabla}_{col}_boxplot.png"))
        plt.show()
        plt.close()

        # 2. Distribución Facetada (Separando escalas)
        g = sns.FacetGrid(df, col="Categoria", sharex=False, sharey=False, height=5, aspect=1.2)
        g.map(sns.histplot, col, kde=True, color="darkblue")
        g.set_titles("{col_name}")
        plt.savefig(os.path.join(direct_graficos, f"{nombre_tabla}_{col}_distribucion.png"))
        plt.show()
        plt.close()

def limpieza_avanzada_segmentada(df):
    """Calcula Z-scores independientes por categoría"""
    if 'Categoria' not in df.columns:
        return df
    
    df_limpio = []
    for cat in df['Categoria'].unique():
        sub_df = df[df['Categoria'] == cat].copy()
        
        for col in sub_df.select_dtypes(include=[np.number]).columns:
            if col in ['id', 'ID_Prod']: continue
            
            mean = sub_df[col].mean()
            std = sub_df[col].std()
            if std == 0: continue
            
            # Z-Score por categoría: $Z = \frac{x - \mu_{cat}}{\sigma_{cat}}$[cite: 1]
            z_scores = np.abs((sub_df[col] - mean) / std)
            
            # Regresión a la media segmentada
            outliers_45 = (z_scores > 4.5) & (z_scores <= 7)
            if np.issubdtype(sub_df[col].dtype, np.integer):
                sub_df.loc[outliers_45, col] = int(round(mean))
            else:
                sub_df.loc[outliers_45, col] = mean
                
            # Eliminar errores críticos (Z > 7)
            sub_df = sub_df[z_scores <= 7]
            
        df_limpio.append(sub_df)
    
    return pd.concat(df_limpio, ignore_index=True)

# --- EJECUCIÓN PRINCIPAL ---
def ejecutar_proceso():
    # Conexión SQL (Igual que antes)[cite: 1]
    engine = sa.create_engine(f"mssql+pyodbc://@LAPTOP-OFP910OT/Surcomotor_DB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

    for tabla in ["tabla_ventas", "tabla_compras"]:
        path = os.path.join(direct_base, f"{tabla}.csv")
        df = pd.read_csv(path, encoding='utf-8-sig')
        
        # Clasificar y Limpiar
        df['Categoria'] = df['Producto'].apply(categorizar_producto)
        df = limpieza_avanzada_segmentada(df)
        
        # EDA y Carga
        generar_eda_segmentado(df, tabla)
        df.to_sql(tabla, engine, if_exists='replace', index=False)
        print(f"Tabla {tabla} procesada con éxito por categorías.")

ejecutar_proceso()