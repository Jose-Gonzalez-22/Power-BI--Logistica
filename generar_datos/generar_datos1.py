import pandas as pd

# Crea directamente las tablas de productos y almacenes (no necesita simulación)
PRODUCTOS = [
    {"id": 1, "desc": "AUTO HONDA ACCORD 2014", "nombre": "ACCORD", "tipo": "AUTOS",
     "foto": "https://i.postimg.cc/k5vFNbnt/2023-Honda-Accord-Exterior-1024x630.jpg"},
    # ... (resto igual que en tu código original) ...
]
ALMACENES = [
    {"id": 1, "nombre": "SURCO", "cap_v": 35, "cap_r": 100, "ubicacion": "Surco, Lima"},
    {"id": 2, "nombre": "LA MOLINA", "cap_v": 20, "cap_r": 250, "ubicacion": "La Molina, Lima"}
]

df_prod = pd.DataFrame([{
    "ID_PRODUCTO": p["id"], "DESCRIPCIÓN": p["desc"],
    "NOMBRE": p["nombre"], "TIPO": p["tipo"], "FOTO": p["foto"]
} for p in PRODUCTOS])
df_alm = pd.DataFrame([{
    "id_almacen": a["id"], "almacen": a["nombre"],
    "Capacidad Vehiculos": a["cap_v"], "Capacidad Repuestos": a["cap_r"],
    "ubicacion": a["ubicacion"]
} for a in ALMACENES])

df_prod.to_csv("tabla_productos.csv", index=False, encoding="utf-8-sig")
df_alm.to_csv("tabla_almacenes.csv", index=False, encoding="utf-8-sig")
print("✅ Productos y almacenes guardados.")