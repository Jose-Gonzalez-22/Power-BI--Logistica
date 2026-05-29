import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import urllib
import os

# ==============================================
# 1. CONFIGURACIÓN DE CONEXIÓN
# ==============================================
SERVER = "LAPTOP-OFP910OT"
DATABASE = "Surcomotor_DB"

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + SERVER +
    ";DATABASE=" + DATABASE + ";Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

print("✅ Conexión establecida con SQL Server")

# ==============================================
# 2. DEFINICIÓN DE TABLAS Y SUS CLAVES PRIMARIAS
# ==============================================
tablas_definicion = {
    "productos": {
        "columnas": {
            "ID_PRODUCTO": "INT PRIMARY KEY",
            "DESCRIPCIÓN": "NVARCHAR(255)",
            "NOMBRE": "NVARCHAR(100)",
            "TIPO": "NVARCHAR(50)",
            "FOTO": "NVARCHAR(MAX)"
        },
        "archivo": "productos.csv"
    },
    "almacenes": {
        "columnas": {
            "id_almacen": "INT PRIMARY KEY",
            "almacen": "NVARCHAR(100)",
            "capacidad_vehiculos": "INT",
            "capacidad_repuestos": "INT",
            "ubicacion": "NVARCHAR(255)"
        },
        "archivo": "almacenes.csv"
    },
    "proveedores": {
        "columnas": {
            "id_proveedor": "INT PRIMARY KEY",
            "nombre": "NVARCHAR(255)",
            "tipo": "NVARCHAR(50)"
        },
        "archivo": "proveedores.csv"
    },
    "vendedores": {
        "columnas": {
            "id_vendedor": "INT PRIMARY KEY",
            "nombre": "NVARCHAR(255)"
        },
        "archivo": "vendedores.csv"
    },
    "clientes": {
        "columnas": {
            "id_cliente": "INT PRIMARY KEY",
            "cliente": "NVARCHAR(255)",
            "segmento": "NVARCHAR(50)"
        },
        "archivo": "clientes.csv"
    },
    "precios_costos_mensuales": {
        "columnas": {
            "id_producto": "INT",
            "producto": "NVARCHAR(255)",
            "mes": "DATE",
            "precio_compra": "DECIMAL(18,2)",
            "precio_venta": "DECIMAL(18,2)"
        },
        "pk": "PRIMARY KEY (id_producto, mes)",
        "archivo": "precios_costos_mensuales.csv"
    },
    "compras": {
        "columnas": {
            "id_compra": "INT PRIMARY KEY",
            "fecha": "DATE",
            "id_proveedor": "INT",
            "proveedor": "NVARCHAR(255)",
            "id_almacen": "INT",
            "almacen": "NVARCHAR(100)",
            "id_producto": "INT",
            "producto": "NVARCHAR(255)",
            "cantidad": "INT",
            "precio_compra": "DECIMAL(18,2)",
            "monto": "DECIMAL(18,2)"
        },
        "archivo": "compras.csv"
    },
    "ventas": {
        "columnas": {
            "id_venta": "INT PRIMARY KEY",
            "fecha": "DATE",
            "id_cliente": "INT",
            "id_almacen": "INT",
            "id_producto": "INT",
            "producto": "NVARCHAR(255)",
            "cantidad": "INT",
            "precio_venta": "DECIMAL(18,2)",
            "monto": "DECIMAL(18,2)",
            "id_vendedor": "INT"
        },
        "archivo": "ventas.csv"
    },
    "movimientos_stock": {
        "columnas": {
            "Fecha": "DATE",
            "Tipo": "NVARCHAR(100)",
            "Almacen": "NVARCHAR(100)",
            "ID_Producto": "INT",
            "Producto": "NVARCHAR(255)",
            "Cantidad_Stock": "INT"
        },
        "pk": None,
        "archivo": "movimientos_stock.csv",
        "agregar_id": True
    }
}

# Carpeta donde buscar los archivos si no están en el directorio actual
CARPETA_DATOS = "Datos"

# ==============================================
# 3. CREAR TABLAS, LIMPIARLAS Y CARGAR DATOS
# ==============================================
with engine.connect() as conn:
    for nombre_tabla, defs in tablas_definicion.items():
        archivo = defs["archivo"]
        # Buscar archivo en la carpeta actual o en Datos/
        ruta_archivo = archivo
        if not os.path.exists(ruta_archivo):
            ruta_alternativa = os.path.join(CARPETA_DATOS, archivo)
            if os.path.exists(ruta_alternativa):
                ruta_archivo = ruta_alternativa
            else:
                print(f"⚠️ Archivo {archivo} no encontrado (ni en ./ ni en {CARPETA_DATOS}/), saltando tabla {nombre_tabla}")
                continue

        print(f"⏳ Procesando {ruta_archivo} -> tabla {nombre_tabla}...")

        df = pd.read_csv(ruta_archivo, encoding='utf-8-sig')
        for col in df.columns:
            if 'fecha' in col.lower() or 'mes' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col], dayfirst=False)
                except:
                    pass

        df.columns = [col.strip() for col in df.columns]

        columnas_sql = []
        pk_def = defs.get("pk", None)
        agregar_id = defs.get("agregar_id", False)

        if agregar_id:
            columnas_sql.append("[id_movimiento_stock] INT IDENTITY(1,1) PRIMARY KEY")

        for col_name, col_type in defs["columnas"].items():
            columnas_sql.append(f"[{col_name}] {col_type}")

        if pk_def and not agregar_id:
            columnas_sql.append(pk_def)

        create_sql = f"IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{nombre_tabla}' AND schema_id = SCHEMA_ID('dbo'))\n"
        create_sql += f"CREATE TABLE dbo.{nombre_tabla} (\n"
        create_sql += ",\n".join(columnas_sql)
        create_sql += "\n);"

        conn.execute(text(create_sql))
        conn.commit()

        # Limpiar tabla antes de insertar
        conn.execute(text(f"TRUNCATE TABLE {nombre_tabla}"))
        conn.commit()

        df.to_sql(nombre_tabla, conn, if_exists='append', index=False, method=None, chunksize=1000)
        print(f"   → {len(df)} filas insertadas en {nombre_tabla}")

print("\n✅ Todas las tablas dimensionales y de hechos cargadas y limpiadas")

# ==============================================
# 4. CREAR Y POBLAR LA TABLA "entidades"
# ==============================================
with engine.connect() as conn:
    conn.execute(text("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'entidades' AND schema_id = SCHEMA_ID('dbo'))
        BEGIN
            CREATE TABLE dbo.entidades (
                id_entidad INT IDENTITY(1,1) PRIMARY KEY,
                nombre NVARCHAR(255) NOT NULL,
                tipo NVARCHAR(50) NOT NULL,
                segmento NVARCHAR(50) NULL
            );
        END;
    """))
    conn.commit()

    conn.execute(text("TRUNCATE TABLE entidades"))
    conn.commit()
    print("✅ Tabla 'entidades' creada y limpiada")

    conn.execute(text("""
        INSERT INTO entidades (nombre, tipo, segmento)
        SELECT cliente AS nombre,
               segmento AS tipo,
               segmento AS segmento
        FROM clientes;
    """))
    conn.commit()
    print("   → Clientes insertados en entidades")

    conn.execute(text("""
        INSERT INTO entidades (nombre, tipo, segmento)
        SELECT nombre, 'Empresa', NULL
        FROM proveedores;
    """))
    conn.commit()
    print("   → Proveedores insertados en entidades")

# ==============================================
# 5. CREAR Y POBLAR TABLA UNIFICADA "movimientos"
# ==============================================
with engine.connect() as conn:
    # Crear tabla
    conn.execute(text("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'movimientos' AND schema_id = SCHEMA_ID('dbo'))
        BEGIN
            CREATE TABLE dbo.movimientos (
                id_movimiento INT IDENTITY(1,1) PRIMARY KEY,
                TipoMovimiento NVARCHAR(255),
                Fecha DATE,
                Entidad NVARCHAR(255),
                Almacen NVARCHAR(255),
                Producto NVARCHAR(255),
                Cantidad INT,
                CostoUnitario DECIMAL(18,2),
                PrecioUnitario DECIMAL(18,2),
                Monto DECIMAL(18,2),
                Vendedor NVARCHAR(255)
            );
        END;
    """))
    conn.commit()

    conn.execute(text("TRUNCATE TABLE movimientos"))
    conn.commit()
    print("✅ Tabla 'movimientos' creada y limpiada")

    # -------------------------------------------
    # Ventas
    # -------------------------------------------
    conn.execute(text("""
        INSERT INTO movimientos (TipoMovimiento, Fecha, Entidad, Almacen, Producto, Cantidad, CostoUnitario, PrecioUnitario, Monto, Vendedor)
        SELECT 
            'Venta',
            v.fecha,
            c.cliente,
            a.almacen,
            v.producto,
            v.cantidad,
            pcm.precio_compra AS CostoUnitario,
            pcm.precio_venta AS PrecioUnitario,
            v.monto,
            ve.nombre
        FROM ventas v
        LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
        LEFT JOIN almacenes a ON v.id_almacen = a.id_almacen
        LEFT JOIN vendedores ve ON v.id_vendedor = ve.id_vendedor
        LEFT JOIN precios_costos_mensuales pcm 
            ON pcm.id_producto = v.id_producto 
            AND pcm.mes = DATEFROMPARTS(YEAR(v.fecha), MONTH(v.fecha), 1);
    """))
    conn.commit()
    print("✅ Ventas insertadas en movimientos")

    # -------------------------------------------
    # Compras
    # -------------------------------------------
    conn.execute(text("""
        INSERT INTO movimientos (TipoMovimiento, Fecha, Entidad, Almacen, Producto, Cantidad, CostoUnitario, PrecioUnitario, Monto, Vendedor)
        SELECT 
            'Compra',
            c.fecha,
            p.nombre,
            a.almacen,
            c.producto,
            c.cantidad,
            c.precio_compra AS CostoUnitario,
            pcm.precio_venta AS PrecioUnitario,
            c.monto,
            NULL
        FROM compras c
        LEFT JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        LEFT JOIN almacenes a ON c.id_almacen = a.id_almacen
        LEFT JOIN precios_costos_mensuales pcm 
            ON pcm.id_producto = c.id_producto 
            AND pcm.mes = DATEFROMPARTS(YEAR(c.fecha), MONTH(c.fecha), 1);
    """))
    conn.commit()
    print("✅ Compras insertadas en movimientos")

    # -------------------------------------------
    # Movimientos de stock
    # -------------------------------------------
    conn.execute(text("""
        INSERT INTO movimientos (TipoMovimiento, Fecha, Entidad, Almacen, Producto, Cantidad, CostoUnitario, PrecioUnitario, Monto, Vendedor)
        SELECT 
            s.Tipo,
            s.Fecha,
            NULL AS Entidad,
            s.Almacen,
            s.Producto,
            s.Cantidad_Stock,
            pcm.precio_compra AS CostoUnitario,
            CASE 
                WHEN s.Tipo = 'Salida' THEN pcm.precio_venta
                ELSE NULL
            END AS PrecioUnitario,
            CASE 
                WHEN s.Tipo IN ('Entrada', 'Control Stock diario', 'Cierre de Stock general') 
                    THEN s.Cantidad_Stock * pcm.precio_compra
                WHEN s.Tipo = 'Salida' 
                    THEN s.Cantidad_Stock * pcm.precio_venta
                ELSE NULL
            END AS Monto,
            NULL
        FROM movimientos_stock s
        LEFT JOIN precios_costos_mensuales pcm 
            ON pcm.id_producto = s.ID_Producto 
            AND pcm.mes = DATEFROMPARTS(YEAR(s.Fecha), MONTH(s.Fecha), 1);
    """))
    conn.commit()
    print("✅ Movimientos de stock insertados en movimientos")

print("\n🎉 Proceso finalizado. Consulta: SELECT * FROM movimientos ORDER BY Fecha, id_movimiento;")