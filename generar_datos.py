import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import math

# -------------------------------
# 1. DATOS MAESTROS (según documento)
# -------------------------------

PRODUCTOS = [
    {"id": 1, "desc": "AUTO HONDA ACCORD 2014", "nombre": "ACCORD", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/k5vFNbnt/2023-Honda-Accord-Exterior-1024x630.jpg"},
    {"id": 2, "desc": "AUTO HONDA CIVIC 2014", "nombre": "CIVIC", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "http://tse1.mm.bing.net/th?q=Honda%20Civic%20LX"},
    {"id": 3, "desc": "AUTO HONDA ODISSEY 2013", "nombre": "ODISSEY", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/pdfk0SBr/2021-honda-odyssey-293-1598917033.jpg"},
    {"id": 4, "desc": "AUTO HONDA CRV 2014", "nombre": "CRV", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/43djjsmy/10best-trucks-suvs-2023-honda-crv-113-1673298616.jpg"},
    {"id": 5, "desc": "AUTO HONDA PILOT 2013", "nombre": "PILOT", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/SQCcFP2f/RT-V-0b9e0d030f58483f92da6152bddf8210.webp"},
    {"id": 6, "desc": "AUTO HONDA FIT 2016", "nombre": "FIT", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/3JqLWmR8/2020-honda-fit-mmp-1-1574789897.jpg"},
    {"id": 7, "desc": "AUTO HONDA CITY 2016", "nombre": "CITY", "tipo": "AUTOS",
     "media_v": 4, "std_v": 2, "m_p": 17000, "std_p": 2000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/xTQM0PLD/Galeria-CITY-Gris-1.webp"},
    {"id": 8, "desc": "CAMIONETA HONDA ELEMENT 2013", "nombre": "ELEMENT", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/QdtBtYtP/descarga.jpg"},
    {"id": 9, "desc": "CAMIONETA HONDA CROSSTOUR 2013", "nombre": "CROSSTOUR", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/KznjVdqK/OOHOGEC1.webp"},
    {"id": 10, "desc": "CAMIONETA HONDA CR-Z 2015", "nombre": "CR-Z", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/PxM3q7L9/1366-2000.jpg"},
    {"id": 11, "desc": "CAMIONETA HONDA RID LINE PICK UP 2014", "nombre": "RID LINE", "tipo": "CAMIONETAS",
     "media_v": 3, "std_v": 1, "m_p": 24000, "std_p": 3000, "dur_p": (2,1), "m_mv": 1.5, "std_mv": 0.2, "dur_mv": (2,1),
     "foto": "https://i.postimg.cc/4dG2sG3p/1366-2000-1.jpg"},
    {"id": 38, "desc": "ACEITE DE MOTOR 5W30 FULL SINTÉTICO", "nombre": "ACEITE 5W30", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "m_p": 100, "std_p": 10, "dur_p": (1,0), "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/13d7fT9Y/3679497-01.jpg"},
    {"id": 39, "desc": "FILTRO DE COMBUSTIBLE", "nombre": "FILTRO", "tipo": "REPUESTOS",
     "media_v": 10, "std_v": 5, "m_p": 100, "std_p": 10, "dur_p": (1,0), "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/25FWPbXF/filtro-de-gasolina.jpg"},
    {"id": 40, "desc": "AMORTIGUADORES DELANTEROS", "nombre": "AMORT DEL", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "m_p": 220, "std_p": 15, "dur_p": (1,0), "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/d3zmqMR8/51l-A0-RBe-YNL-AC-UF894-1000-QL80.jpg"},
    {"id": 41, "desc": "AMORTIGUADORES POSTERIORES", "nombre": "AMORT POS", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "m_p": 90, "std_p": 10, "dur_p": (1,0), "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/vB24sW79/amortiguador-sfx-jpmotorcycles-ASFX.jpg"},
    {"id": 42, "desc": "LLANTAS 18\"", "nombre": "LLANTAS 18\"", "tipo": "REPUESTOS",
     "media_v": 100, "std_v": 25, "m_p": 60, "std_p": 10, "dur_p": (1,0), "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/YCV4ZN3W/image-Url-1.webp"},
    {"id": 43, "desc": "BATERÍA DE 18 PLACAS", "nombre": "BATERÍA 18 PLC", "tipo": "REPUESTOS",
     "media_v": 50, "std_v": 10, "m_p": 90, "std_p": 10, "dur_p": (1,0), "m_mv": 1.2, "std_mv": 0.1, "dur_mv": (1,0),
     "foto": "https://i.postimg.cc/DZ4S7SxM/baterias-capsa-13wi-min.jpg"}
]

ALMACENES = [
    {"id": 1, "nombre": "SURCO", "cap_v": 35, "cap_r": 100, "ubicacion": "Surco, Lima"},
    {"id": 2, "nombre": "LA MOLINA", "cap_v": 20, "cap_r": 250, "ubicacion": "La Molina, Lima"}
]

VENDEDORES = [f"Vendedor {i+1}" for i in range(10)]

# Clientes iniciales (se irán creando dinámicamente si es necesario, pero fijamos 50)
clientes = []
for i in range(50):
    tipo = random.choice(["Persona", "Empresa"])
    clientes.append({
        "id": i+1,
        "nombre": f"Cliente {i+1}",
        "segmento": tipo,
        "gasto_anual_actual": 0,
        "anio_actual": None   # se controlará en la simulación
    })

# -------------------------------
# 2. FUNCIONES AUXILIARES
# -------------------------------

def trunc_norm_int(mean, std, min_val=0):
    """Devuelve entero >= min_val con distribución normal truncada"""
    val = int(np.random.normal(mean, std))
    return max(min_val, val)

def generar_precio_con_persistencia(prod):
    """Retorna (precio, duracion_meses, markup, duracion_markup)"""
    precio = max(0, np.random.normal(prod["m_p"], prod["std_p"]))
    dur_precio = max(1, int(np.random.normal(prod["dur_p"][0], prod["dur_p"][1])))
    markup = max(0, np.random.normal(prod["m_mv"], prod["std_mv"]))
    dur_markup = max(1, int(np.random.normal(prod["dur_mv"][0], prod["dur_mv"][1])))
    return precio, dur_precio, markup, dur_markup

def obtener_capacidad_restante(almacen, stock_actual, pedidos_pendientes, es_vehiculo):
    """Calcula el espacio disponible en el almacén para vehículos o repuestos."""
    tipo = "v" if es_vehiculo else "r"
    cap_max = almacen["cap_v"] if es_vehiculo else almacen["cap_r"]
    ocupado = stock_actual
    # sumar pedidos pendientes que aún no han llegado
    for ped in pedidos_pendientes:
        if ped["almacen_id"] == almacen["id"] and ped["es_vehiculo"] == es_vehiculo:
            ocupado += ped["cantidad"]
    return max(0, cap_max - ocupado)

# -------------------------------
# 3. SIMULACIÓN PRINCIPAL
# -------------------------------

np.random.seed(42)   # reproducibilidad
random.seed(42)

# Estructuras de estado
stock = {alm["id"]: {p["id"]: 0 for p in PRODUCTOS} for alm in ALMACENES}
precios_actuales = {}      # {prod_id: (precio, meses_rest_precio, markup, meses_rest_markup)}
pedidos_pendientes = []    # cada pedido: {"fecha_llegada", "almacen_id", "producto_id", "cantidad", "es_vehiculo"}

compras = []   # lista de dicts para tabla compras
ventas = []    # lista de dicts para tabla ventas
stock_historial = []   # controles de inventario (14 y fin de mes)

# Fechas
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime(2025, 12, 31)
delta = fecha_fin - fecha_inicio
dias_totales = delta.days + 1

# ----- COMPRA INICIAL (llenar 85% de cada almacén) -----
# Para cada almacén, determinamos cuántos vehículos totales y cuántos repuestos totales debemos tener
for almacen in ALMACENES:
    # Vehículos (autos + camionetas)
    cap_v = almacen["cap_v"]
    objetivo_v = int(cap_v * 0.85)          # número total de vehículos a almacenar inicialmente
    # Repuestos
    cap_r = almacen["cap_r"]
    objetivo_r = int(cap_r * 0.85)          # número total de repuestos

    # Lista de productos vehículos (ids)
    ids_vehiculos = [p["id"] for p in PRODUCTOS if p["tipo"] in ("AUTOS","CAMIONETAS")]
    # Lista de repuestos
    ids_repuestos = [p["id"] for p in PRODUCTOS if p["tipo"] == "REPUESTOS"]

    # Distribuir objetivo_v entre los vehículos de forma aleatoria pero respetando que la suma sea exacta
    cant_vehiculos = [0] * len(ids_vehiculos)
    for _ in range(objetivo_v):
        idx = random.randrange(len(ids_vehiculos))
        cant_vehiculos[idx] += 1

    # Distribuir objetivo_r entre repuestos
    cant_repuestos = [0] * len(ids_repuestos)
    for _ in range(objetivo_r):
        idx = random.randrange(len(ids_repuestos))
        cant_repuestos[idx] += 1

    # Asignar stock inicial directamente (sin pedido, asumimos que ya está en almacén.
    # Esto es para empezar a vender desde el día 1. La condición "compra inicial con retraso"
    # haría que los primeros 25 días no haya vehículos, lo cual es poco realista.
    # En su lugar, damos el stock inicial como si ya hubiera llegado.
    for i, prod_id in enumerate(ids_vehiculos):
        stock[almacen["id"]][prod_id] = cant_vehiculos[i]
    for i, prod_id in enumerate(ids_repuestos):
        stock[almacen["id"]][prod_id] = cant_repuestos[i]

    # Registrar la compra inicial en la tabla de compras (con fecha -1 para indicar que fue antes de empezar)
    fecha_compra_inicial = fecha_inicio - timedelta(days=1)   # un día antes
    for i, prod_id in enumerate(ids_vehiculos):
        if cant_vehiculos[i] > 0:
            prod = next(p for p in PRODUCTOS if p["id"] == prod_id)
            # Precio de compra: generamos uno con persistencia pero lo guardamos
            precio, dur_p, markup, dur_m = generar_precio_con_persistencia(prod)
            # Guardamos el precio para usarlo durante los próximos meses
            precios_actuales[prod_id] = (precio, dur_p, markup, dur_m)
            monto = cant_vehiculos[i] * precio
            compras.append({
                "id_compra": len(compras)+1,
                "Fecha": fecha_compra_inicial,
                "Proveedor": "Prov Vehículos",
                "Almacen": almacen["nombre"],
                "Producto": prod["desc"],
                "Cantidad": cant_vehiculos[i],
                "Precio_Compra": round(precio,2),
                "Monto": round(monto,2)
            })
    for i, prod_id in enumerate(ids_repuestos):
        if cant_repuestos[i] > 0:
            prod = next(p for p in PRODUCTOS if p["id"] == prod_id)
            precio, dur_p, markup, dur_m = generar_precio_con_persistencia(prod)
            precios_actuales[prod_id] = (precio, dur_p, markup, dur_m)
            monto = cant_repuestos[i] * precio
            compras.append({
                "id_compra": len(compras)+1,
                "Fecha": fecha_compra_inicial,
                "Proveedor": "Prov Repuestos",
                "Almacen": almacen["nombre"],
                "Producto": prod["desc"],
                "Cantidad": cant_repuestos[i],
                "Precio_Compra": round(precio,2),
                "Monto": round(monto,2)
            })

# Para los productos que no se compraron inicialmente, generamos sus precios por si acaso
for prod in PRODUCTOS:
    if prod["id"] not in precios_actuales:
        precio, dur_p, markup, dur_m = generar_precio_con_persistencia(prod)
        precios_actuales[prod["id"]] = (precio, dur_p, markup, dur_m)

# ----- SIMULACIÓN DÍA A DÍA -----
fecha_actual = fecha_inicio
ultimo_cierre_mes_stock_cero = {prod["id"]: False for prod in PRODUCTOS}  # para regla de no dos meses seguidos con stock=0 al cierre

# Para controlar gasto anual de clientes
def reiniciar_gasto_clientes(nuevo_anio):
    for c in clientes:
        if c["anio_actual"] != nuevo_anio:
            c["gasto_anual_actual"] = 0
            c["anio_actual"] = nuevo_anio

while fecha_actual <= fecha_fin:
    dia = fecha_actual.day
    mes = fecha_actual.month
    anio = fecha_actual.year
    reiniciar_gasto_clientes(anio)

    # 1. Llegada de pedidos pendientes
    for pedido in pedidos_pendientes[:]:
        if pedido["fecha_llegada"] <= fecha_actual:
            # Verificar capacidad antes de añadir
            almacen = next(alm for alm in ALMACENES if alm["id"] == pedido["almacen_id"])
            es_veh = pedido["es_vehiculo"]
            stock_actual_prod = stock[pedido["almacen_id"]][pedido["producto_id"]]
            # Capacidad total usada en esa categoría
            if es_veh:
                ocupado_actual = sum(stock[pedido["almacen_id"]][pid] for pid in [p["id"] for p in PRODUCTOS if p["tipo"] in ("AUTOS","CAMIONETAS")])
                cap_max = almacen["cap_v"]
            else:
                ocupado_actual = sum(stock[pedido["almacen_id"]][pid] for pid in [p["id"] for p in PRODUCTOS if p["tipo"] == "REPUESTOS"])
                cap_max = almacen["cap_r"]
            espacio_libre = cap_max - ocupado_actual
            cant_a_recibir = min(pedido["cantidad"], espacio_libre)
            if cant_a_recibir > 0:
                stock[pedido["almacen_id"]][pedido["producto_id"]] += cant_a_recibir
            # Si sobra cantidad por falta de espacio, se pierde (en realidad no debería pasar si controlamos antes)
            pedidos_pendientes.remove(pedido)

    # 2. Controles de inventario (14 y último día del mes)
    es_fin_mes = (fecha_actual + timedelta(days=1)).month != mes
    if dia == 14 or es_fin_mes:
        for alm in ALMACENES:
            for prod in PRODUCTOS:
                stock_historial.append({
                    "Fecha": fecha_actual,
                    "Almacen": alm["nombre"],
                    "ID_Producto": prod["id"],
                    "Producto": prod["nombre"],
                    "Cantidad_Stock": stock[alm["id"]][prod["id"]]
                })

    # 3. Compras (días 1 y 15, pero no el primer día si ya hicimos compra inicial)
    if (dia in (1, 15)) and not (fecha_actual == fecha_inicio and dia==1):
        # Actualizar duración de precios y markups (al comenzar el mes, pero lo hacemos aquí)
        # Lo ideal sería al inicio de cada mes, pero como compramos 1 y 15, reducimos solo si es día 1
        if dia == 1:
            for prod_id in list(precios_actuales.keys()):
                precio, dur_p, markup, dur_m = precios_actuales[prod_id]
                if dur_p > 0:
                    dur_p -= 1
                if dur_m > 0:
                    dur_m -= 1
                if dur_p <= 0 or dur_m <= 0:
                    # Generar nuevos valores
                    prod = next(p for p in PRODUCTOS if p["id"] == prod_id)
                    nuevo_precio, nueva_dur_p, nuevo_markup, nueva_dur_m = generar_precio_con_persistencia(prod)
                    if dur_p <= 0:
                        precio = nuevo_precio
                        dur_p = nueva_dur_p
                    if dur_m <= 0:
                        markup = nuevo_markup
                        dur_m = nueva_dur_m
                precios_actuales[prod_id] = (precio, dur_p, markup, dur_m)

        # Lógica de compra por producto y almacén
        for alm in ALMACENES:
            for prod in PRODUCTOS:
                es_vehiculo = prod["tipo"] in ("AUTOS","CAMIONETAS")
                # Calcular stock actual y stock mínimo para no quedarnos sin stock
                stock_actual = stock[alm["id"]][prod["id"]]
                # Demanda media mensual
                demanda_media = prod["media_v"]   # unidades mes
                tiempo_reposicion = 25 if es_vehiculo else 2  # días
                # Convertir a meses aprox
                meses_repos = tiempo_reposicion / 30.0
                stock_seguridad = int(demanda_media * meses_repos * 1.5)  # factor de seguridad
                # Además, forzar compra si el producto cerró el mes pasado con stock=0
                if ultimo_cierre_mes_stock_cero[prod["id"]]:
                    # Necesitamos evitar que ocurra dos veces seguidas, así que compramos al menos 1 unidad
                    stock_seguridad = max(stock_seguridad, 1)

                capacidad_disponible = obtener_capacidad_restante(alm, 
                    sum(stock[alm["id"]][pid] for pid in [p["id"] for p in PRODUCTOS if (p["tipo"] in ("AUTOS","CAMIONETAS")) == es_vehiculo]),
                    pedidos_pendientes, es_vehiculo)
                if capacidad_disponible <= 0:
                    continue

                # Cantidad a comprar para alcanzar stock_seguridad, sin superar capacidad
                cantidad_deseada = max(0, stock_seguridad - stock_actual)
                if cantidad_deseada == 0:
                    continue
                cantidad_comprar = min(cantidad_deseada, capacidad_disponible)
                if cantidad_comprar == 0:
                    continue

                precio_compra, _, markup, _ = precios_actuales[prod["id"]]
                monto = cantidad_comprar * precio_compra
                proveedor = "Prov Vehículos" if es_vehiculo else "Prov Repuestos"
                compras.append({
                    "id_compra": len(compras)+1,
                    "Fecha": fecha_actual,
                    "Proveedor": proveedor,
                    "Almacen": alm["nombre"],
                    "Producto": prod["desc"],
                    "Cantidad": cantidad_comprar,
                    "Precio_Compra": round(precio_compra,2),
                    "Monto": round(monto,2)
                })

                # Registrar pedido pendiente
                fecha_llegada = fecha_actual + timedelta(days=tiempo_reposicion)
                pedidos_pendientes.append({
                    "fecha_llegada": fecha_llegada,
                    "almacen_id": alm["id"],
                    "producto_id": prod["id"],
                    "cantidad": cantidad_comprar,
                    "es_vehiculo": es_vehiculo
                })

    # 4. Ventas (generar demanda mensual y distribuir)
    # Para simplificar y cumplir la aleatoriedad mensual, al inicio de cada mes generamos la demanda total por producto y la repartimos a lo largo del mes.
    # Esto lo haremos en el día 1 de cada mes.
    if dia == 1:
        demanda_mensual = {}  # {producto_id: cantidad total a vender en el mes}
        for prod in PRODUCTOS:
            demanda = trunc_norm_int(prod["media_v"], prod["std_v"])
            # Ajustar regla de no dos meses seguidos con stock cero
            # Si el mes pasado cerró con stock=0 Y la demanda es muy alta, forzamos a que no se agote este mes
            # pero eso se gestiona en la ejecución diaria. Aquí solo generamos demanda
            demanda_mensual[prod["id"]] = demanda
        # Guardar esta demanda para el mes
        dias_en_mes = (fecha_actual.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        dias_mes = dias_en_mes.day
        # Distribución diaria: asignamos cuotas diarias, el último día el remanente
        ventas_diarias_meta = {prod["id"]: max(1, demanda // dias_mes) if demanda>0 else 0 for prod in PRODUCTOS}
        remanente = {prod["id"]: demanda % dias_mes for prod in PRODUCTOS}
        # Lo guardamos en un diccionario para ir consumiendo durante el mes
        dias_restantes = dias_mes
    # En cada día, usamos la distribución
    if dia == 1:
        # Creamos un registro de ventas pendientes para el mes
        ventas_pendientes_mes = {prod["id"]: demanda_mensual[prod["id"]] for prod in PRODUCTOS}
    # Por cada día, intentamos vender una parte de la demanda pendiente
    for prod in PRODUCTOS:
        if ventas_pendientes_mes[prod["id"]] <= 0:
            continue
        # Cantidad a vender hoy = mínimo entre lo pendiente y la cuota diaria (o 1 si es el último día)
        cuota_hoy = max(1, ventas_pendientes_mes[prod["id"]] // max(1, dias_restantes))
        cuota_hoy = min(cuota_hoy, ventas_pendientes_mes[prod["id"]])
        # Ajuste aleatorio para que no sea uniforme perfecto
        cuota_hoy = random.randint(1, cuota_hoy) if cuota_hoy > 1 else cuota_hoy
        if cuota_hoy == 0:
            continue
        # Buscar clientes y almacenes
        # Elegir un almacén que tenga stock
        almacenes_con_stock = [alm for alm in ALMACENES if stock[alm["id"]][prod["id"]] > 0]
        if not almacenes_con_stock:
            # No hay stock, no se vende nada hoy de este producto
            continue
        almacen = random.choice(almacenes_con_stock)
        # Capacidad de venta por cliente
        cliente = random.choice(clientes)
        max_por_transaccion = 5 if prod["tipo"] in ("AUTOS","CAMIONETAS") else 10
        if cliente["segmento"] == "Empresa":
            max_por_transaccion = 20 if prod["tipo"] in ("AUTOS","CAMIONETAS") else 40
        max_gasto_anual = 1_000_000 if cliente["segmento"] == "Persona" else 10_000_000
        # Cuánto podemos vender realmente
        cant_vender = min(cuota_hoy, stock[almacen["id"]][prod["id"]], max_por_transaccion)
        # Verificar límite de gasto anual
        precio_compra, _, markup, _ = precios_actuales[prod["id"]]
        precio_venta = precio_compra * markup
        monto_venta = cant_vender * precio_venta
        if cliente["gasto_anual_actual"] + monto_venta > max_gasto_anual:
            # Reducir cantidad hasta que quepa en el presupuesto
            max_gasto_restante = max_gasto_anual - cliente["gasto_anual_actual"]
            if max_gasto_restante <= 0:
                continue
            cant_vender = min(cant_vender, int(max_gasto_restante // precio_venta))
            if cant_vender <= 0:
                continue
            monto_venta = cant_vender * precio_venta

        if cant_vender > 0:
            stock[almacen["id"]][prod["id"]] -= cant_vender
            cliente["gasto_anual_actual"] += monto_venta
            ventas_pendientes_mes[prod["id"]] -= cant_vender
            ventas.append({
                "id_venta": len(ventas)+1,
                "Fecha": fecha_actual,
                "Cliente": cliente["nombre"],
                "Almacen": almacen["nombre"],
                "Producto": prod["desc"],
                "Cantidad_Vendida": cant_vender,
                "Precio_Venta": round(precio_venta,2),
                "Monto_Venta": round(monto_venta,2),
                "Vendedor": random.choice(VENDEDORES)
            })
    # Actualizar días restantes del mes
    if dia == 1:
        dias_restantes = dias_mes - 1
    else:
        dias_restantes -= 1

    # Al final del día, si es fin de mes, actualizar el flag de stock cero
    if es_fin_mes:
        for prod in PRODUCTOS:
            stock_total = sum(stock[alm["id"]][prod["id"]] for alm in ALMACENES)
            if stock_total == 0:
                # Si ya había sido cero el mes anterior, eso es violación. Para evitarlo forzamos una compra antes, pero ya lo hicimos en la compra condicional
                # Simplemente registramos el flag
                ultimo_cierre_mes_stock_cero[prod["id"]] = True
            else:
                ultimo_cierre_mes_stock_cero[prod["id"]] = False

    fecha_actual += timedelta(days=1)

# -------------------------------
# 4. CREACIÓN DE DATAFRAMES Y EXPORTACIÓN
# -------------------------------

df_compras = pd.DataFrame(compras)
df_ventas = pd.DataFrame(ventas)
df_stock = pd.DataFrame(stock_historial)

df_productos = pd.DataFrame([{
    "ID_PRODUCTO": p["id"],
    "DESCRIPCIÓN": p["desc"],
    "NOMBRE": p["nombre"],
    "TIPO": p["tipo"],
    "FOTO": p["foto"]
} for p in PRODUCTOS])

df_almacenes = pd.DataFrame([{
    "id_almacen": a["id"],
    "almacen": a["nombre"],
    "Capacidad Vehiculos": a["cap_v"],
    "Capacidad Repuestos": a["cap_r"],
    "ubicacion": a["ubicacion"]
} for a in ALMACENES])

df_clientes = pd.DataFrame([{
    "id_cliente": c["id"],
    "Cliente": c["nombre"],
    "segmento": c["segmento"]
} for c in clientes])

# Exportar a CSV
df_compras.to_csv("tabla_compras.csv", index=False, encoding="utf-8-sig")
df_ventas.to_csv("tabla_ventas.csv", index=False, encoding="utf-8-sig")
df_stock.to_csv("tabla_stock_inventario.csv", index=False, encoding="utf-8-sig")
df_productos.to_csv("tabla_productos.csv", index=False, encoding="utf-8-sig")
df_almacenes.to_csv("tabla_almacenes.csv", index=False, encoding="utf-8-sig")
df_clientes.to_csv("tabla_clientes.csv", index=False, encoding="utf-8-sig")

print("Simulación completada.")
print(f"✅ Compras registradas: {len(df_compras)}")
print(f"✅ Ventas registradas: {len(df_ventas)}")
print(f"✅ Controles de stock: {len(df_stock)}")