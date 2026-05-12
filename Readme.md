<!-- README generado automáticamente: versión en español -->
# Power BI - Logística

Resumen breve
---------------
Proyecto para el análisis de datos logísticos que combina procesamiento y limpieza con Python (Jupyter Notebook) y un dashboard interactivo en Power BI.

Estado
------
- Código principal: Jupyter Notebook y scripts en `Datos/`.
- Dashboard: Power BI files en `dashboard pbi/`.

Estructura principal (solo archivos documentados)
-----------------------------------------------
- `EDAyLoad.ipynb` : Notebook principal de EDA, limpieza y transformaciones.
- `Datos/` : Carpeta con ficheros CSV (raw y _clean), y scripts útiles:
  - `Datos/unir_datos.py` : Consolida archivos incrementales en los CSV maestros.
  - CSV importantes: `tabla_ventas.csv`, `tabla_compras.csv`, `tabla_stock_inventario.csv`, `tabla_productos.csv`, `tabla_clientes.csv`, `tabla_almacenes.csv` (y sus versiones `_clean` / `_pred`).
- `dashboard pbi/` : Proyecto Power BI (archivo `.pbip`, modelo semántico y definición del reporte).
- `Imagenes/Readme/` : Diagramas y SVG que explican el flujo de datos y arquitectura.

Exclusiones
-----------
Según `.gitignore`, los siguientes items se excluyen explícitamente de la documentación y no están descritos en detalle aquí:

- `generar_datos/` (carpeta ignorada)
- `auxiliar.xlsx`
- `Material de Clase`

Instalación rápida y ejecución
------------------------------
Se recomienda usar un entorno virtual. Ejemplo en Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install jupyter pandas numpy matplotlib seaborn sqlalchemy
```

Abrir y ejecutar el Notebook:

```powershell
jupyter notebook
# luego abrir EDAyLoad.ipynb y ejecutar celdas
```

Abrir el dashboard de Power BI:

1. Abrir `dashboard pbi/dashboard_Surcomotor.pbip` con Power BI Desktop o Power BI (Fabric).
2. Refrescar los orígenes de datos si la información ha sido actualizada por el Notebook.

Descripción rápida de scripts clave
----------------------------------
- `EDAyLoad.ipynb`: contiene funciones de limpieza (`limpiar_solo_duplicados`) y EDA (`eda_tabla_hechos`), y variables de configuración como `DIRECT_BASE` (ruta base a `Datos generados/`) y listas `TABLAS_HECHOS`, `TABLAS_MAESTRAS`.
- `Datos/unir_datos.py`: busca archivos con sufijo `_add*.csv`, concatena y los anexa al CSV maestro, moviendo los incrementales a `Procesados/`.

Esquema de datos (resumen)
-------------------------
- `tabla_ventas.csv` : columnas típicas: `id_venta, Fecha, Cliente, Almacen, Producto, Cantidad_Vendida, Precio_Venta, Monto_Venta, Vendedor`.
- `tabla_compras.csv` : `id_compra, Fecha, Proveedor, Almacen, Producto, Cantidad, Precio_Compra, Monto`.
- `tabla_stock_inventario.csv` : `Fecha, Tipo, Almacen, ID_Producto, Producto, Cantidad_Stock, Entidad`.
- `tabla_productos.csv` : `ID_PRODUCTO, DESCRIPCIÓN, NOMBRE, TIPO, FOTO`.
- `tabla_clientes.csv` : `id_cliente, Cliente, segmento`.
- `tabla_almacenes.csv` : `id_almacen, almacen, Capacidad Vehiculos, Capacidad Repuestos, ubicacion`.

Notas y recomendaciones
-----------------------
- Revisar y ajustar `DIRECT_BASE` en `EDAyLoad.ipynb` para que apunte a la carpeta donde están los CSV (por ejemplo `C:/Proyectos/Power BI - Logística/Datos generados/`).
- Antes de ejecutar el Notebook, validar encoding y separadores de los CSV (`utf-8-sig` usado en el proyecto).
- Mantener los archivos excluidos fuera del repositorio según `.gitignore`.

Contribuciones
--------------
Si quieres mejorar la documentación o el código:

1. Haz fork del repositorio.
2. Crea una rama con tu cambio.
3. Abre un pull request describiendo los cambios.

Contacto
--------
Para dudas o reportes, abre un issue en el repositorio.