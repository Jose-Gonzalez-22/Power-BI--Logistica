import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# --- 1. CONFIGURACIÓN DE PRODUCTOS Y ALMACENES (Según instrucciones) ---
# Se asume que las definiciones de PRODUCTOS y ALMACENES son las mismas del docx

direct_base = "C:/Proyectos/Power BI - Logística/Datos generados/"

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

def cargar_y_actualizar_mes():
    try:
        # Cargar datos existentes para mantener continuidad
        df_ventas = pd.read_csv(os.path.join(direct_base, 'tabla_ventas.csv'))
        df_compras = pd.read_csv(os.path.join(direct_base, 'tabla_compras.csv'))
        df_stock_hist = pd.read_csv(os.path.join(direct_base, 'tabla_stock_inventario.csv'))
        df_clientes = pd.read_csv(os.path.join(direct_base, 'tabla_clientes.csv'))
        
        # Determinar última fecha y siguiente mes
        ultima_fecha = pd.to_datetime(df_ventas['Fecha']).max()
        fecha_inicio_mes = (ultima_fecha + relativedelta(months=1)).replace(day=1)
        fecha_fin_mes = (fecha_inicio_mes + relativedelta(months=1)) - timedelta(days=1)
        
        print(f"Generando datos para: {fecha_inicio_mes.strftime('%B %Y')}")

        # --- 2. RECUPERAR ESTADO DEL STOCK ---
        # Obtenemos el último control de inventario disponible
        ultimo_stock = df_stock_hist[df_stock_hist['Fecha'] == df_stock_hist['Fecha'].max()]
        stock_actual = {}
        for alm in ALMACENES:
            stock_actual[alm['id']] = {
                p['id']: ultimo_stock[(ultimo_stock['Almacen'] == alm['nombre']) & 
                                     (ultimo_stock['ID_Prod'] == p['id'])]['Stock'].values[0] 
                for p in PRODUCTOS
            }

        # --- 3. SIMULACIÓN DEL MES ---
        nuevas_ventas = []
        nuevas_compras = []
        nuevos_controles = []
        pedidos_en_transito = [] # Lógica de retrasos

        vendedores = [f"Vendedor {i+1}" for i in range(10)]
        
        # Bucle diario
        for dia_idx in range((fecha_fin_mes - fecha_inicio_mes).days + 1):
            fecha_hoy = fecha_inicio_mes + timedelta(days=dia_idx)
            dia = fecha_hoy.day

            # A. Llegada de pedidos previos (Vehículos 25 días, Repuestos 2 días)
            for pedido in pedidos_en_transito[:]:
                if pedido['llega'] <= fecha_hoy:
                    stock_actual[pedido['alm']][pedido['prod']] += pedido['cant']
                    pedidos_en_transito.remove(pedido)

            # B. Compras (Días 1 y 15)[cite: 1]
            if dia in [1, 15]:
                for p in PRODUCTOS:
                    for alm in ALMACENES:
                        es_v = p['tipo'] in ["AUTOS", "CAMIONETAS"]
                        # Lógica: Si el stock bajó del 40% de la cuota asignada, reponer al 85%[cite: 1]
                        cap_total = alm['cap_v'] if es_v else alm['cap_r']
                        n_tipos = len([x for x in PRODUCTOS if x['tipo'] == p['tipo']])
                        cuota = int((cap_total * 0.85) / n_tipos)
                        
                        if stock_actual[alm['id']][p['id']] < (cuota * 0.4):
                            cant_c = cuota - stock_actual[alm['id']][p['id']]
                            precio_c = np.random.normal(p['m_p'], p['std_p'])
                            nuevas_compras.append({
                                "id": len(df_compras) + len(nuevas_compras) + 1,
                                "Fecha": fecha_hoy, "Proveedor": "Prov_Gral",
                                "Almacen": alm['nombre'], "Producto": p['desc'],
                                "Cant": cant_c, "Precio_C": precio_c, "Monto": cant_c * precio_c
                            })
                            pedidos_en_transito.append({
                                "llega": fecha_hoy + timedelta(days=25 if es_v else 2),
                                "alm": alm['id'], "prod": p['id'], "cant": cant_c
                            })

            # C. Ventas Diarias
            for p in PRODUCTOS:
                v_hoy = max(0, int(np.random.normal(p['media_v']/30, p['std_v']/10)))
                for _ in range(v_hoy):
                    alm_v = random.choice(ALMACENES)
                    if stock_actual[alm_v['id']][p['id']] > 0:
                        # Probabilidad de nuevo cliente (20%)
                        if random.random() < 0.05:
                            nuevo_id = df_clientes['id'].max() + 1
                            nuevo_c = {"id": nuevo_id, "Cliente": f"Nuevo Cliente {nuevo_id}", 
                                       "Segmento": random.choice(["Persona", "Empresa"])}
                            df_clientes = pd.concat([df_clientes, pd.DataFrame([nuevo_c])])
                        
                        cli = df_clientes.sample(1).iloc[0]
                        cant_v = 1 # Venta unitaria para simplificar stock real
                        precio_v = np.random.normal(p['m_p'], p['std_p']) * 1.5 # Margen[cite: 1]
                        
                        stock_actual[alm_v['id']][p['id']] -= cant_v
                        nuevas_ventas.append({
                            "id": len(df_ventas) + len(nuevas_ventas) + 1,
                            "Fecha": fecha_hoy, "Cliente": cli['Cliente'],
                            "Almacen": alm_v['nombre'], "Producto": p['desc'],
                            "Cant": cant_v, "Precio_V": precio_v, "Monto": cant_v * precio_v,
                            "Vendedor": random.choice(vendedores)
                        })

            # D. Control de Inventario (Día 14 y Fin de Mes)[cite: 1]
            if dia == 14 or fecha_hoy == fecha_fin_mes:
                for alm in ALMACENES:
                    for p in PRODUCTOS:
                        nuevos_controles.append({
                            "Fecha": fecha_hoy, "Almacen": alm['nombre'],
                            "ID_Prod": p['id'], "Producto": p['nombre'],
                            "Stock": stock_actual[alm['id']][p['id']]
                        })

        # --- 4. GUARDAR CAMBIOS (APPEND) ---
        pd.DataFrame(nuevas_ventas).to_csv('tabla_ventas_add.csv', mode='a', header=False, index=False)
        pd.DataFrame(nuevas_compras).to_csv('tabla_compras_add.csv', mode='a', header=False, index=False)
        pd.DataFrame(nuevos_controles).to_csv('tabla_stock_inventario_add.csv', mode='a', header=False, index=False)
        df_clientes.to_csv('tabla_clientes_add.csv', index=False)

        print(f"Carga completa para {fecha_inicio_mes.strftime('%m/%Y')}. Ventas: {len(nuevas_ventas)}")

    except FileNotFoundError:
        print("Error: No se encontraron los archivos base. Genera primero los 3 años iniciales.")

# Ejecutar carga del nuevo mes
cargar_y_actualizar_mes()