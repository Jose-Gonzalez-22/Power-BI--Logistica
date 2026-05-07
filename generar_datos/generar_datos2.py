import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================================
# 1. DATOS MAESTROS
# ============================================================
PRODUCTOS = [
    # AUTOS
    {"id": 1, "desc": "AUTO HONDA ACCORD 2014", "nombre": "ACCORD", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/k5vFNbnt/2023-Honda-Accord-Exterior-1024x630.jpg",
     "es_vehiculo": True},
    {"id": 2, "desc": "AUTO HONDA CIVIC 2014", "nombre": "CIVIC", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "http://tse1.mm.bing.net/th?q=Honda%20Civic%20LX",
     "es_vehiculo": True},
    {"id": 3, "desc": "AUTO HONDA ODISSEY 2013", "nombre": "ODISSEY", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/pdfk0SBr/2021-honda-odyssey-293-1598917033.jpg",
     "es_vehiculo": True},
    {"id": 4, "desc": "AUTO HONDA CRV 2014", "nombre": "CRV", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/43djjsmy/10best-trucks-suvs-2023-honda-crv-113-1673298616.jpg",
     "es_vehiculo": True},
    {"id": 5, "desc": "AUTO HONDA PILOT 2013", "nombre": "PILOT", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/SQCcFP2f/RT-V-0b9e0d030f58483f92da6152bddf8210.webp",
     "es_vehiculo": True},
    {"id": 6, "desc": "AUTO HONDA FIT 2016", "nombre": "FIT", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/3JqLWmR8/2020-honda-fit-mmp-1-1574789897.jpg",
     "es_vehiculo": True},
    {"id": 7, "desc": "AUTO HONDA CITY 2016", "nombre": "CITY", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "multiple_v": 1,
     "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/xTQM0PLD/Galeria-CITY-Gris-1.webp",
     "es_vehiculo": True},
    # CAMIONETAS
    {"id": 8, "desc": "CAMIONETA HONDA ELEMENT 2013", "nombre": "ELEMENT", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "multiple_v": 1,
     "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/QdtBtYtP/descarga.jpg",
     "es_vehiculo": True},
    {"id": 9, "desc": "CAMIONETA HONDA CROSSTOUR 2013", "nombre": "CROSSTOUR", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "multiple_v": 1,
     "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/KznjVdqK/OOHOGEC1.webp",
     "es_vehiculo": True},
    {"id": 10, "desc": "CAMIONETA HONDA CR-Z 2015", "nombre": "CR-Z", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "multiple_v": 1,
     "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/PxM3q7L9/1366-2000.jpg",
     "es_vehiculo": True},
    {"id": 11, "desc": "CAMIONETA HONDA RID LINE PICK UP 2014", "nombre": "RID LINE", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "multiple_v": 1,
     "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "multiple_p": 500,
     "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/4dG2sG3p/1366-2000-1.jpg",
     "es_vehiculo": True},
    # REPUESTOS
    {"id": 38, "desc": "ACEITE DE MOTOR 5W30 FULL SINTÉTICO", "nombre": "ACEITE FS 5W30", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "multiple_v": 1,
     "m_p": 100, "std_p": 10, "dur_p": (1,0), "multiple_p": 1,
     "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/13d7fT9Y/3679497-01.jpg",
     "es_vehiculo": False},
    {"id": 39, "desc": "FILTRO DE COMBUSTIBLE", "nombre": "FILTRO COMBUST", "tipo": "REPUESTOS",
     "media_v": 10, "std_v": 5, "multiple_v": 1,
     "m_p": 100, "std_p": 10, "dur_p": (1,0), "multiple_p": 1,
     "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/25FWPbXF/filtro-de-gasolina.jpg",
     "es_vehiculo": False},
    {"id": 40, "desc": "AMORTIGUADORES DELANTEROS", "nombre": "AMORT DEL", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "multiple_v": 1,
     "m_p": 220, "std_p": 15, "dur_p": (1,0), "multiple_p": 1,
     "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/d3zmqMR8/51l-A0-RBe-YNL-AC-UF894-1000-QL80.jpg",
     "es_vehiculo": False},
    {"id": 41, "desc": "AMORTIGUADORES POSTERIORES", "nombre": "AMORT POS", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "multiple_v": 1,
     "m_p": 90, "std_p": 10, "dur_p": (1,0), "multiple_p": 1,
     "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/vB24sW79/amortiguador-sfx-jpmotorcycles-ASFX.jpg",
     "es_vehiculo": False},
    {"id": 42, "desc": "LLANTAS 18\"", "nombre": "LLANTAS 18\"", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "multiple_v": 1,
     "m_p": 60, "std_p": 10, "dur_p": (1,0), "multiple_p": 1,
     "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/YCV4ZN3W/image-Url-1.webp",
     "es_vehiculo": False},
    {"id": 43, "desc": "BATERÍA DE 18 PLACAS", "nombre": "BATERÍA 18 PLC", "tipo": "REPUESTOS",
     "media_v": 50, "std_v": 10, "multiple_v": 1,
     "m_p": 90, "std_p": 10, "dur_p": (1,0), "multiple_p": 1,
     "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/DZ4S7SxM/baterias-capsa-13wi-min.jpg",
     "es_vehiculo": False}
]

ALMACENES = [
    {"id": 1, "nombre": "SURCO", "cap_v": 35, "cap_r": 100, "ubicacion": "Surco, Lima"},
    {"id": 2, "nombre": "LA MOLINA", "cap_v": 20, "cap_r": 250, "ubicacion": "La Molina, Lima"}
]

VENDEDORES = [f"Vendedor {i+1}" for i in range(10)]

# Clientes iniciales
clientes = []
for i in range(50):
    clientes.append({
        "id": i+1,
        "nombre": f"Cliente {i+1}",
        "segmento": random.choice(["Persona", "Empresa"]),
        "gasto_anual_actual": 0,
        "anio_actual": None
    })

# ============================================================
# 2. FUNCIONES AUXILIARES
# ============================================================

def normal_round_to_multiple(mean, std, multiple):
    val = np.random.normal(mean, std)
    if multiple == 1:
        return max(0, int(round(val)))
    else:
        return max(0, int(round(val / multiple)) * multiple)

def normal_int(mean, std, multiple=1):
    return normal_round_to_multiple(mean, std, multiple)

def generar_precio_con_persistencia(prod):
    precio = normal_round_to_multiple(prod["m_p"], prod["std_p"], prod["multiple_p"])
    dur_precio = max(1, int(np.random.normal(prod["dur_p"][0], prod["dur_p"][1])))
    markup = max(0.01, np.random.normal(prod["m_mv"], prod["std_mv"]))
    dur_markup = max(1, int(np.random.normal(prod["dur_mv"][0], prod["dur_mv"][1])))
    return precio, dur_precio, markup, dur_markup

def generar_demanda_mensual(prod):
    return normal_int(prod["media_v"], prod["std_v"], prod["multiple_v"])

def obtener_capacidad_restante(almacen, stock_actual, pedidos_pendientes, es_vehiculo):
    cap_max = almacen["cap_v"] if es_vehiculo else almacen["cap_r"]
    ocupado = stock_actual
    for ped in pedidos_pendientes:
        if ped["almacen_id"] == almacen["id"] and ped["es_vehiculo"] == es_vehiculo:
            ocupado += ped["cantidad"]
    return max(0, cap_max - ocupado)

def reiniciar_gasto_clientes(anio):
    for c in clientes:
        if c["anio_actual"] != anio:
            c["gasto_anual_actual"] = 0
            c["anio_actual"] = anio

# ============================================================
# 3. PREPARACIÓN DE ESTRUCTURAS
# ============================================================

np.random.seed(42)
random.seed(42)

# Diccionarios para acceso rápido
prod_dict = {p["id"]: p for p in PRODUCTOS}
ids_vehiculos = [p["id"] for p in PRODUCTOS if p["es_vehiculo"]]
ids_repuestos = [p["id"] for p in PRODUCTOS if not p["es_vehiculo"]]
prods_vehiculo = [p for p in PRODUCTOS if p["es_vehiculo"]]
prods_repuesto = [p for p in PRODUCTOS if not p["es_vehiculo"]]

stock = {alm["id"]: {pid: 0 for pid in prod_dict} for alm in ALMACENES}
precios_actuales = {}
pedidos_pendientes = []
compras = []
ventas = []
stock_historial = []

# ============================================================
# 4. COMPRA INICIAL
# ============================================================

fecha_compra_inicial = datetime(2023, 1, 1) - timedelta(days=1)

for almacen in ALMACENES:
    obj_v = int(almacen["cap_v"] * 0.85)
    obj_r = int(almacen["cap_r"] * 0.85)

    # Distribuir vehículos aleatoriamente
    cant_v = {pid: 0 for pid in ids_vehiculos}
    for _ in range(obj_v):
        pid = random.choice(ids_vehiculos)
        cant_v[pid] += 1

    cant_r = {pid: 0 for pid in ids_repuestos}
    for _ in range(obj_r):
        pid = random.choice(ids_repuestos)
        cant_r[pid] += 1

    # Asignar stock
    for pid, c in cant_v.items():
        stock[almacen["id"]][pid] = c
    for pid, c in cant_r.items():
        stock[almacen["id"]][pid] = c

    # Registrar compras iniciales
    for pid, c in cant_v.items():
        if c == 0: continue
        prod = prod_dict[pid]
        precio, dur_p, markup, dur_m = generar_precio_con_persistencia(prod)
        precios_actuales[pid] = (precio, dur_p, markup, dur_m)
        compras.append({
            "id_compra": len(compras)+1,
            "Fecha": fecha_compra_inicial,
            "Proveedor": "Prov Vehículos",
            "Almacen": almacen["nombre"],
            "Producto": prod["desc"],
            "Cantidad": c,
            "Precio_Compra": precio,
            "Monto": round(c * precio, 2)
        })

    for pid, c in cant_r.items():
        if c == 0: continue
        prod = prod_dict[pid]
        precio, dur_p, markup, dur_m = generar_precio_con_persistencia(prod)
        precios_actuales[pid] = (precio, dur_p, markup, dur_m)
        compras.append({
            "id_compra": len(compras)+1,
            "Fecha": fecha_compra_inicial,
            "Proveedor": "Prov Repuestos",
            "Almacen": almacen["nombre"],
            "Producto": prod["desc"],
            "Cantidad": c,
            "Precio_Compra": precio,
            "Monto": round(c * precio, 2)
        })

# Precios para productos sin stock inicial
for prod in PRODUCTOS:
    if prod["id"] not in precios_actuales:
        precios_actuales[prod["id"]] = generar_precio_con_persistencia(prod)

# ============================================================
# 5. REGISTRO INICIAL DE INVENTARIO (Entrada + Control)
# ============================================================

fecha_inicio = datetime(2023, 1, 1)
for alm in ALMACENES:
    for prod in PRODUCTOS:
        cant = stock[alm["id"]][prod["id"]]
        if cant > 0:
            stock_historial.append({
                "Fecha": fecha_inicio,
                "Tipo": "Entrada",
                "Almacen": alm["nombre"],
                "ID_Producto": prod["id"],
                "Producto": prod["nombre"],
                "Cantidad_Stock": cant,
                "Entidad": "Prov Vehículos" if prod["es_vehiculo"] else "Prov Repuestos"
            })
        stock_historial.append({
            "Fecha": fecha_inicio,
            "Tipo": "Control",
            "Almacen": alm["nombre"],
            "ID_Producto": prod["id"],
            "Producto": prod["nombre"],
            "Cantidad_Stock": stock[alm["id"]][prod["id"]],
            "Entidad": ""
        })

# ============================================================
# 6. SIMULACIÓN DÍA A DÍA
# ============================================================

fecha_actual = fecha_inicio
fecha_fin = datetime(2025, 12, 31)
ultimo_cierre_stock_cero = {pid: False for pid in prod_dict}
ventas_pendientes_mes = {pid: 0 for pid in prod_dict}
dias_restantes = 0

print("Iniciando simulación día a día...")

while fecha_actual <= fecha_fin:
    dia = fecha_actual.day
    mes = fecha_actual.month
    anio = fecha_actual.year
    reiniciar_gasto_clientes(anio)

    # --- 6.1 Llegada de pedidos (ENTRADA) ---
    i = 0
    while i < len(pedidos_pendientes):
        ped = pedidos_pendientes[i]
        if ped["fecha_llegada"] <= fecha_actual:
            alm = ALMACENES[ped["almacen_id"]-1]
            es_veh = ped["es_vehiculo"]
            if es_veh:
                ocupado = sum(stock[ped["almacen_id"]][p["id"]] for p in prods_vehiculo)
                cap = alm["cap_v"]
            else:
                ocupado = sum(stock[ped["almacen_id"]][p["id"]] for p in prods_repuesto)
                cap = alm["cap_r"]
            espacio = cap - ocupado
            recibir = min(ped["cantidad"], espacio)
            if recibir > 0:
                pid = ped["producto_id"]
                stock[ped["almacen_id"]][pid] += recibir
                prod = prod_dict[pid]
                stock_historial.append({
                    "Fecha": fecha_actual,
                    "Tipo": "Entrada",
                    "Almacen": alm["nombre"],
                    "ID_Producto": pid,
                    "Producto": prod["nombre"],
                    "Cantidad_Stock": recibir,
                    "Entidad": ped["proveedor"]
                })
            pedidos_pendientes.pop(i)
        else:
            i += 1

    # --- 6.2 Compras (días 1 y 15) ---
    if dia in (1, 15) and not (fecha_actual == fecha_inicio and dia == 1):
        if dia == 1:
            for pid in precios_actuales:
                precio, dur_p, markup, dur_m = precios_actuales[pid]
                if dur_p > 0: dur_p -= 1
                if dur_m > 0: dur_m -= 1
                if dur_p <= 0 or dur_m <= 0:
                    prod = prod_dict[pid]
                    nuevo_precio, ndp, nuevo_markup, ndm = generar_precio_con_persistencia(prod)
                    if dur_p <= 0:
                        precio, dur_p = nuevo_precio, ndp
                    if dur_m <= 0:
                        markup, dur_m = nuevo_markup, ndm
                precios_actuales[pid] = (precio, dur_p, markup, dur_m)

        for alm in ALMACENES:
            for prod in PRODUCTOS:
                es_veh = prod["es_vehiculo"]
                stock_actual_prod = stock[alm["id"]][prod["id"]]
                demanda_media = prod["media_v"]
                tiempo_repos = 25 if es_veh else 2
                meses_repos = tiempo_repos / 30.0
                stock_seguridad = int(demanda_media * meses_repos * 1.5)
                if ultimo_cierre_stock_cero[prod["id"]]:
                    stock_seguridad = max(stock_seguridad, 1)

                ocupado_tipo = sum(stock[alm["id"]][p["id"]] for p in (prods_vehiculo if es_veh else prods_repuesto))
                cap_libre = obtener_capacidad_restante(alm, ocupado_tipo, pedidos_pendientes, es_veh)
                if cap_libre <= 0: continue

                cant_deseada = max(0, stock_seguridad - stock_actual_prod)
                if cant_deseada == 0: continue
                cant_comprar = min(cant_deseada, cap_libre)
                if cant_comprar == 0: continue

                precio_compra, _, _, _ = precios_actuales[prod["id"]]
                proveedor = "Prov Vehículos" if es_veh else "Prov Repuestos"
                compras.append({
                    "id_compra": len(compras)+1,
                    "Fecha": fecha_actual,
                    "Proveedor": proveedor,
                    "Almacen": alm["nombre"],
                    "Producto": prod["desc"],
                    "Cantidad": cant_comprar,
                    "Precio_Compra": precio_compra,
                    "Monto": round(cant_comprar * precio_compra, 2)
                })
                fecha_llegada = fecha_actual + timedelta(days=tiempo_repos)
                pedidos_pendientes.append({
                    "fecha_llegada": fecha_llegada,
                    "almacen_id": alm["id"],
                    "producto_id": prod["id"],
                    "cantidad": cant_comprar,
                    "es_vehiculo": es_veh,
                    "proveedor": proveedor
                })

    # --- 6.3 Ventas (SALIDA) ---
    if dia == 1:
        demandas_mensuales = {p["id"]: generar_demanda_mensual(p) for p in PRODUCTOS}
        ventas_pendientes_mes = demandas_mensuales.copy()
        siguiente_mes = fecha_actual.replace(day=28) + timedelta(days=4)
        fin_mes = siguiente_mes.replace(day=1) - timedelta(days=1)
        dias_mes = fin_mes.day
        dias_restantes = dias_mes

    if dias_restantes <= 0:
        dias_restantes = 1

    for prod in PRODUCTOS:
        pend = ventas_pendientes_mes[prod["id"]]
        if pend <= 0: continue

        cuota = max(1, pend // dias_restantes)
        cuota = min(cuota, pend)
        if cuota > 1:
            cuota = random.randint(1, cuota)

        almacenes_stock = [a for a in ALMACENES if stock[a["id"]][prod["id"]] > 0]
        if not almacenes_stock:
            continue
        almacen = random.choice(almacenes_stock)

        cliente = random.choice(clientes)
        max_trans = 5 if prod["es_vehiculo"] else 10
        if cliente["segmento"] == "Empresa":
            max_trans = 20 if prod["es_vehiculo"] else 40
        max_gasto = 1_000_000 if cliente["segmento"] == "Persona" else 10_000_000

        cant_vender = min(cuota, stock[almacen["id"]][prod["id"]], max_trans)
        precio_compra, _, markup, _ = precios_actuales[prod["id"]]
        pv_raw = precio_compra * markup
        precio_venta = round(pv_raw / 500) * 500 if prod["es_vehiculo"] else round(pv_raw, 1)
        monto = cant_vender * precio_venta

        if cliente["gasto_anual_actual"] + monto > max_gasto:
            restante = max_gasto - cliente["gasto_anual_actual"]
            if restante <= 0: continue
            cant_vender = min(cant_vender, int(restante // precio_venta))
            if cant_vender <= 0: continue
            monto = cant_vender * precio_venta

        if cant_vender > 0:
            stock[almacen["id"]][prod["id"]] -= cant_vender
            cliente["gasto_anual_actual"] += monto
            ventas_pendientes_mes[prod["id"]] -= cant_vender

            ventas.append({
                "id_venta": len(ventas)+1,
                "Fecha": fecha_actual,
                "Cliente": cliente["nombre"],
                "Almacen": almacen["nombre"],
                "Producto": prod["desc"],
                "Cantidad_Vendida": cant_vender,
                "Precio_Venta": precio_venta,
                "Monto_Venta": round(monto, 2),
                "Vendedor": random.choice(VENDEDORES)
            })
            stock_historial.append({
                "Fecha": fecha_actual,
                "Tipo": "Salida",
                "Almacen": almacen["nombre"],
                "ID_Producto": prod["id"],
                "Producto": prod["nombre"],
                "Cantidad_Stock": cant_vender,
                "Entidad": cliente["nombre"]
            })

    dias_restantes -= 1

    # --- 6.4 Controles de inventario (día 14 y fin de mes) ---
    es_fin_mes = (fecha_actual + timedelta(days=1)).month != mes
    if dia == 14 or es_fin_mes:
        for alm in ALMACENES:
            for prod in PRODUCTOS:
                stock_historial.append({
                    "Fecha": fecha_actual,
                    "Tipo": "Control",
                    "Almacen": alm["nombre"],
                    "ID_Producto": prod["id"],
                    "Producto": prod["nombre"],
                    "Cantidad_Stock": stock[alm["id"]][prod["id"]],
                    "Entidad": ""
                })

    if es_fin_mes:
        for pid in prod_dict:
            total = sum(stock[alm_id][pid] for alm_id in stock)
            ultimo_cierre_stock_cero[pid] = (total == 0)

    fecha_actual += timedelta(days=1)

# ============================================================
# 7. EXPORTACIÓN A CSV
# ============================================================

print("Exportando tablas...")
df_compras = pd.DataFrame(compras)
df_ventas = pd.DataFrame(ventas)
df_stock = pd.DataFrame(stock_historial)

df_productos = pd.DataFrame([{
    "ID_PRODUCTO": p["id"], "DESCRIPCIÓN": p["desc"],
    "NOMBRE": p["nombre"], "TIPO": p["tipo"], "FOTO": p["foto"]
} for p in PRODUCTOS])

df_almacenes = pd.DataFrame([{
    "id_almacen": a["id"], "almacen": a["nombre"],
    "Capacidad Vehiculos": a["cap_v"], "Capacidad Repuestos": a["cap_r"],
    "ubicacion": a["ubicacion"]
} for a in ALMACENES])

df_clientes = pd.DataFrame([{
    "id_cliente": c["id"], "Cliente": c["nombre"], "segmento": c["segmento"]
} for c in clientes])

(df_ventas.to_csv("tabla_ventas.csv", index=False, encoding="utf-8-sig"),
 df_clientes.to_csv("tabla_clientes.csv", index=False, encoding="utf-8-sig"))

print("Simulación completada.")
print(f"✅ Ventas: {len(df_ventas)}")