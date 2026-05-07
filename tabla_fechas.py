import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlalchemy as sa

# Configuración de fechas (2014 a 2018)
FECHA_INICIO = datetime(2022, 1, 1)
FECHA_FIN = datetime(2026, 12, 31)

# Nombres en español
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
MESES_ABR = {
    1: "ene", 2: "feb", 3: "mar", 4: "abr",
    5: "may", 6: "jun", 7: "jul", 8: "ago",
    9: "sep", 10: "oct", 11: "nov", 12: "dic"
}
DIAS_SEMANA = {
    0: "Domingo", 1: "Lunes", 2: "Martes", 3: "Miércoles",
    4: "Jueves", 5: "Viernes", 6: "Sábado"
}

def generar_tabla_fechas(fecha_ini, fecha_fin):
    """Genera un DataFrame con la estructura final esperada por Power Query."""
    fechas = pd.date_range(start=fecha_ini, end=fecha_fin, freq='D')
    df = pd.DataFrame({'Fecha': fechas})
    
    # Columnas base
    df['Año'] = df['Fecha'].dt.year
    df['Orden Mes'] = df['Fecha'].dt.month           # renombra luego a "Orden Mes"
    df['Mes'] = df['Orden Mes'].map(MESES)
    df['Dia'] = df['Fecha'].dt.day
    
    # Día de semana (domingo = 1)
    df['Orden Dia Semana'] = df['Fecha'].dt.weekday.map(lambda x: 7 if x == 6 else x + 2)
    df['Dia Semana'] = df['Fecha'].dt.weekday.map(DIAS_SEMANA)
    
    # Trimestre
    df['Orden Trimestre'] = df['Fecha'].dt.quarter
    df['Trimestre'] = 'T' + df['Orden Trimestre'].astype(str)
    
    # Periodo (Año*100 + Mes)
    df['Periodo'] = df['Año'] * 100 + df['Orden Mes']
    
    # Año-Mes (nombre propio)
    df['Año-Mes'] = df['Mes'] + ' ' + df['Año'].astype(str)
    
    # aaaa-mmm (minúscula y abreviatura)
    df['aaaa-mmm'] = df['Orden Mes'].map(MESES_ABR) + ' ' + df['Año'].astype(str)
    
    # Inicio de semana (domingo)
    df['Inicio de Semana'] = df['Fecha'] - pd.to_timedelta(df['Orden Dia Semana'] - 1, unit='D')
    
    # Rango de semana
    fin_semana = df['Inicio de Semana'] + timedelta(days=6)
    df['Rango Semana'] = df['Inicio de Semana'].dt.strftime('%d/%m/%Y') + ' - ' + fin_semana.dt.strftime('%d/%m/%Y')
    
    # Clave entera
    df['FechaKey'] = df['Fecha'].dt.strftime('%Y%m%d').astype(int)
    
    # Orden final de columnas (exactamente como en Power Query)
    columnas = [
        'FechaKey', 'Fecha', 'Año', 'Orden Trimestre', 'Trimestre', 'Periodo',
        'Año-Mes', 'aaaa-mmm', 'Orden Mes', 'Mes', 'Dia',
        'Orden Dia Semana', 'Dia Semana', 'Inicio de Semana', 'Rango Semana'
    ]
    df = df[columnas]
    
    # Asegurar tipo date para Inicio de Semana
    df['Inicio de Semana'] = pd.to_datetime(df['Inicio de Semana']).dt.date
    
    return df

# Generar la tabla
df_fechas = generar_tabla_fechas(FECHA_INICIO, FECHA_FIN)
print(f"Tabla de fechas generada: {len(df_fechas)} registros")
print(df_fechas.head(3))

# --- Conexión a SQL Server y carga ---
SERVER = "LAPTOP-OFP910OT"
DATABASE = "Surcomotor_DB"
TABLE_NAME = "Fecha"

conn_str = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = sa.create_engine(conn_str)

df_fechas.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
print(f"✅ Tabla '{TABLE_NAME}' cargada correctamente en la base de datos '{DATABASE}'")