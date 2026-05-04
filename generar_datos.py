import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN INICIAL Y DATOS MAESTROS
PRODUCTOS = [
    {"id": 1, "desc": "AUTO HONDA ACCORD 2014", "nombre": "ACCORD", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 2, "desc": "AUTO HONDA CIVIC 2014", "nombre": "CIVIC", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 3, "desc": "AUTO HONDA ODISSEY 2013", "nombre": "ODISSEY", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 4, "desc": "AUTO HONDA CRV 2014", "nombre": "CRV", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 5, "desc": "AUTO HONDA PILOT 2013", "nombre": "PILOT", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 6, "desc": "AUTO HONDA FIT 2016", "nombre": "FIT", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 7, "desc": "AUTO HONDA CITY 2016", "nombre": "CITY", "tipo": "AUTOS", "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 8, "desc": "CAMIONETA HONDA ELEMENT 2013", "nombre": "ELEMENT", "tipo": "CAMIONETAS", "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 9, "desc": "CAMIONETA HONDA CROSSTOUR 2013", "nombre": "CROSSTOUR", "tipo": "CAMIONETAS", "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 10, "desc": "CAMIONETA HONDA CR-Z 2015", "nombre": "CR-Z", "tipo": "CAMIONETAS", "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 11, "desc": "CAMIONETA HONDA RID LINE PICK UP 2014", "nombre": "RID LINE", "tipo": "CAMIONETAS", "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "m_t": 2, "std_t": 1, "m_mv": 1.5, "std_mv": 0.2},
    {"id": 38, "desc": "ACEITE DE MOTOR 5W30", "nombre": "ACEITE", "tipo": "REPUESTOS", "media_v": 100, "std_v": 25, "m_p": 100, "std_p": 10, "m_t": 1, "std_t": 0, "m_mv": 1.2, "std_mv": 0.1},
    {"id": 39, "desc": "FILTRO DE COMBUSTIBLE", "nombre": "FILTRO", "tipo": "REPUESTOS", "media_v": 10, "std_v": 5, "m_p": 100, "std_p": 10, "m_t": 1, "std_t": 0, "m_mv": 1.2, "std_mv": 0.1},
    {"id": 40, "desc": "AMORTIGUADORES DEL.", "nombre": "AMORT DEL", "tipo": "REPUESTOS", "media_v": 100, "std_v": 25, "m_p": 220, "std_p": 15, "m_t": 1, "std_t": 0, "m_mv": 1.2, "std_mv": 0.1},
    {"id": 41, "desc": "AMORTIGUADORES POST.", "nombre": "AMORT POS", "tipo": "REPUESTOS", "media_v": 100, "std_v": 25, "m_p": 90, "std_p": 10, "m_t": 1, "std_t": 0, "m_mv": 1.2, "std_mv": 0.1},
    {"id": 42, "desc": "LLANTAS 18\"", "nombre": "LLANTAS", "tipo": "REPUESTOS", "media_v": 100, "std_v": 25, "m_p": 60, "std_p": 10, "m_t": 1, "std_t": 0, "m_mv": 1.2, "std_mv": 0.1},
    {"id": 43, "desc": "BATERÍA DE 18 PLACAS", "nombre": "BATERIA", "tipo": "REPUESTOS", "media_v": 50, "std_v": 10, "m_p": 90, "std_p": 10, "m_t": 1, "std_t": 0, "m_mv": 1.2, "std_mv": 0.1}
]

ALMACENES = [
    {"id": 1, "nombre": "SURCO", "cap_v": 35, "cap_r": 100, "ub": "Surco, Lima"},
    {"id": 2, "nombre": "LA MOLINA", "cap_v": 20, "cap_r": 250, "ub": "La Molina, Lima"}
]

VENDEDORES = [f"Vendedor {i+1}" for i in range(10)]
CLIENTES = [{"id": i, "nombre": f"Cliente {i}", "tipo": random.choice(["Persona", "Empresa"]), "gasto_anual": 0} for i in range(50)]

# 2. FUNCIONES DE APOYO
def trunc_norm(mean, std):
    return max(0, int(np.random.normal(mean, std)))

def get_price_info(prod):
    price = np.random.normal(prod['m_p'], prod['std_p'])
    duration = max(1, int(np.random.normal(prod['m_t'], prod['std_t'])))
    markup = np.random.normal(prod['m_mv'], prod['std_mv'])
    return price, duration, markup

# 3. NÚCLEO DE LA SIMULACIÓN
stock = {alm['id']: {p['id']: 0 for p in PRODUCTOS} for alm in ALMACENES}
precios_actuales = {p['id']: {"p": 0, "dur": 0, "m": 0} for p in PRODUCTOS}
pedidos_pendientes = [] # {fecha_llegada, almacen_id, prod_id, cant}

compras_data = []
ventas_data = []
stock_historial = []

fecha_inicio = datetime(2023, 1, 1)
dias_simulacion = 3 * 365

for dia_idx in range(dias_simulacion):
    fecha_actual = fecha_inicio + timedelta(days=dia_idx)
    dia = fecha_actual.day
    mes = fecha_actual.month
    
    # --- A. LLEGADA DE MERCANCÍA ---
    for pedido in pedidos_pendientes[:]:
        if pedido['fecha'] <= fecha_actual:
            stock[pedido['alm']][pedido['prod']] += pedido['cant']
            pedidos_pendientes.remove(pedido)

    # --- B. CONTROL DE INVENTARIO Y COMPRAS (1 y 15) ---
    if dia in [1, 15] or dia_idx == 0:
        for p in PRODUCTOS:
            if precios_actuales[p['id']]["dur"] <= 0:
                p_val, d_val, m_val = get_price_info(p)
                precios_actuales[p['id']] = {"p": p_val, "dur": d_val, "m": m_val}
            
            for alm in ALMACENES:
                # Lógica de compra inicial (85%) o reposición
                es_vehiculo = p['tipo'] in ["AUTOS", "CAMIONETAS"]
                cap_total = alm['cap_v'] if es_vehiculo else alm['cap_r']
                stock_actual = stock[alm['id']][p['id']]
                
                # Para simplificar: distribuimos capacidad entre productos del mismo tipo
                n_prods_tipo = len([x for x in PRODUCTOS if x['tipo'] == p['tipo'] or (es_vehiculo and x['tipo'] in ["AUTOS", "CAMIONETAS"])])
                meta_stock = int((cap_total * 0.85) / n_prods_tipo)
                
                if stock_actual < meta_stock:
                    cant_compra = meta_stock - stock_actual
                    monto = cant_compra * precios_actuales[p['id']]["p"]
                    
                    compras_data.append({
                        "id": len(compras_data)+1, "Fecha": fecha_actual, 
                        "Proveedor": "Prov Vehículos" if es_vehiculo else "Prov Repuestos",
                        "Almacen": alm['nombre'], "Producto": p['desc'], "Cant": cant_compra,
                        "Precio_C": precios_actuales[p['id']]["p"], "Monto": monto
                    })
                    
                    retraso = 25 if es_vehiculo else 2
                    pedidos_pendientes.append({
                        "fecha": fecha_actual + timedelta(days=retraso),
                        "alm": alm['id'], "prod": p['id'], "cant": cant_compra
                    })
        
        if dia == 1: # Reducir duración de precio al inicio de mes
            for p in PRODUCTOS: precios_actuales[p['id']]["dur"] -= 1

    # --- C. CONTROL DE STOCK (14 y Fin de mes) ---
    if dia == 14 or fecha_actual == (fecha_actual.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1):
        for alm in ALMACENES:
            for p in PRODUCTOS:
                stock_historial.append({
                    "Fecha": fecha_actual, "Almacen": alm['nombre'], 
                    "ID_Prod": p['id'], "Producto": p['nombre'], "Stock": stock[alm['id']][p['id']]
                })

    # --- D. VENTAS DIARIAS ---
    # Distribución diaria de la media mensual
    for p in PRODUCTOS:
        ventas_hoy = trunc_norm(p['media_v']/30, p['std_v']/10)
        if ventas_hoy > 0:
            for _ in range(ventas_hoy):
                alm = random.choice(ALMACENES)
                if stock[alm['id']][p['id']] > 0:
                    cli = random.choice(CLIENTES)
                    # Validar límites de cliente
                    es_v = p['tipo'] in ["AUTOS", "CAMIONETAS"]
                    max_u = (5 if es_v else 10) if cli['tipo'] == "Persona" else (20 if es_v else 40)
                    presupuesto = 1000000 if cli['tipo'] == "Persona" else 10000000
                    
                    cant_v = random.randint(1, max_u)
                    cant_v = min(cant_v, stock[alm['id']][p['id']])
                    
                    precio_v = precios_actuales[p['id']]["p"] * precios_actuales[p['id']]["m"]
                    total = cant_v * precio_v
                    
                    if cli['gasto_anual'] + total <= presupuesto:
                        stock[alm['id']][p['id']] -= cant_v
                        cli['gasto_anual'] += total
                        ventas_data.append({
                            "id": len(ventas_data)+1, "Fecha": fecha_actual, "Cliente": cli['nombre'],
                            "Almacen": alm['nombre'], "Producto": p['desc'], "Cant": cant_v,
                            "Precio_V": precio_v, "Monto": total, "Vendedor": random.choice(VENDEDORES)
                        })

# 4. EXPORTACIÓN A DATAFRAMES
df_compras = pd.DataFrame(compras_data)
df_ventas = pd.DataFrame(ventas_data)
df_stock = pd.DataFrame(stock_historial)

print(f"Simulación completada. Ventas generadas: {len(df_ventas)}")
# 5. CREACIÓN DE TABLAS MAESTRAS (Según instrucciones del docx)
df_productos = pd.DataFrame(PRODUCTOS) # Asegúrate de incluir las URLs y IDs exactos del docx
df_almacenes = pd.DataFrame(ALMACENES)
df_clientes_maestro = pd.DataFrame([{"id": c["id"], "Cliente": c["nombre"], "Segmento": c["tipo"]} for c in CLIENTES])

# 6. EXPORTACIÓN A ARCHIVOS CSV
# Usamos index=False para no guardar la columna de índices de pandas
# Usamos encoding='utf-8-sig' para que Excel reconozca tildes y caracteres especiales
df_compras.to_csv('tabla_compras.csv', index=False, encoding='utf-8-sig')
df_ventas.to_csv('tabla_ventas.csv', index=False, encoding='utf-8-sig')
df_stock.to_csv('tabla_stock_inventario.csv', index=False, encoding='utf-8-sig')
df_productos.to_csv('tabla_productos.csv', index=False, encoding='utf-8-sig')
df_almacenes.to_csv('tabla_almacenes.csv', index=False, encoding='utf-8-sig')
df_clientes_maestro.to_csv('tabla_clientes.csv', index=False, encoding='utf-8-sig')

print("Archivos CSV generados exitosamente.")