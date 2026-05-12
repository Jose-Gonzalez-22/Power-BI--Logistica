# Documentación general — Proyecto Power BI - Logística

Última actualización: 2026-05-12

## 1. Propósito

Este documento describe de forma concisa la arquitectura, los scripts y los datos del proyecto "Power BI - Logística". Incluye instrucciones básicas para ejecutar el flujo ETL/EDA y abrir el dashboard en Power BI.

> Nota: se han excluido de esta documentación los archivos y carpetas listados en `.gitignore` (ver sección 2.1).

## 2. Alcance y exclusiones

2.1 Exclusiones (según `.gitignore`)

- `generar_datos/` — carpeta ignorada y no documentada.
- `auxiliar.xlsx` — archivo excluido.
- `Material de Clase` — carpeta excluida.

2.2 Alcance

Documenta los archivos y carpetas presentes en el repositorio que NO están en `.gitignore`: notebooks, scripts bajo `Datos/`, CSV principales, y el proyecto Power BI en `dashboard pbi/`.

## 3. Estructura del proyecto (resumen)

- `EDAyLoad.ipynb` — Notebook principal: import, limpieza, EDA, guardado de versiones `_clean.csv`.
- `Datos/` — CSV de entrada y salida (raw, _clean, _pred) y script `unir_datos.py`.
- `dashboard pbi/` — Proyecto Power BI (.pbip), modelo semántico y definición de report.
- `Imagenes/Readme/` — Diagramas (SVG) que muestran flujo y arquitectura.

## 4. Notebook principal: `EDAyLoad.ipynb`

4.1 Propósito

Realizar carga de datos, limpieza básica (eliminación de duplicados), EDA y generar tablas limpias que consumirá Power BI.

4.2 Variables de configuración relevantes

- `DIRECT_BASE` : ruta base donde se buscan/guardan CSV (configurar según entorno local).
- `SERVER`, `DATABASE` : valores usados si se exporta a SQL Server (opcional).
- `TABLAS_HECHOS` : lista de tablas de hechos que el notebook procesa (por ejemplo `tabla_ventas`, `tabla_compras`, `tabla_stock_inventario`).
- `TABLAS_MAESTRAS` : tablas maestras (productos, almacenes, clientes).

4.3 Funciones clave (resumen)

- `limpiar_solo_duplicados(df, nombre_tabla)` : elimina duplicados exactos y muestra conteo removido.
- `eda_tabla_hechos(df, nombre, columna_tipo=None)` : imprime estadísticas, distribuciones y gráficos (histogramas) por columnas numéricas; si `columna_tipo` está presente, muestra EDA segmentado.

4.4 Salidas

- Para cada tabla procesada suele guardarse un CSV con sufijo `_clean.csv` en la ruta definida por `DIRECT_BASE`.

## 5. Script `Datos/unir_datos.py`

5.1 Propósito

Consolidar ficheros incrementales que tengan patrón `{tabla}_add*.csv` y anexarlos al CSV maestro `{tabla}.csv`. Mueve los incrementales procesados a `Procesados/` añadiendo timestamp.

5.2 Uso

Ejecutar desde la carpeta `Datos/` o desde el root con Python activo en el entorno:

```powershell
python Datos\unir_datos.py
```

5.3 Comportamiento

- Si no hay archivos incrementales para una tabla, no realiza cambios.
- Usa `utf-8-sig` al escribir/leer CSV para mantener compatibilidad con Excel/Power BI.

## 6. CSV principales y esquema (resumen)

- `tabla_ventas.csv` / `_clean.csv` / `_pred.csv`
  - Campos: `id_venta, Fecha, Cliente, Almacen, Producto, Cantidad_Vendida, Precio_Venta, Monto_Venta, Vendedor` (+ `TIPO_PRODUCTO` en versiones _clean).

- `tabla_compras.csv` / `_clean.csv` / `_pred.csv`
  - Campos: `id_compra, Fecha, Proveedor, Almacen, Producto, Cantidad, Precio_Compra, Monto` (+ `TIPO_PRODUCTO` en _clean).

- `tabla_stock_inventario.csv` / `_clean.csv` / `_pred.csv`
  - Campos: `Fecha, Tipo, Almacen, ID_Producto, Producto, Cantidad_Stock, Entidad` (+ `TIPO_PRODUCTO` en _clean).

- `tabla_productos.csv` / `_clean.csv`
  - Campos: `ID_PRODUCTO, DESCRIPCIÓN, NOMBRE, TIPO, FOTO`.

- `tabla_clientes.csv` / `_clean.csv`
  - Campos: `id_cliente, Cliente, segmento`.

- `tabla_almacenes.csv` / `_clean.csv`
  - Campos: `id_almacen, almacen, Capacidad Vehiculos, Capacidad Repuestos, ubicacion`.

## 7. Power BI — `dashboard pbi/`

7.1 Contenido

- `dashboard_Surcomotor.pbip` — descriptor del proyecto.
- `dashboard_Surcomotor.Report/` — definición del informe (JSON), páginas y visuales.
- `dashboard_Surcomotor.SemanticModel/` — modelo semántico, tablas y relaciones (archivos .tmdl y model.tmdl).

7.2 Recomendaciones

- Abrir el `.pbip` con Power BI Desktop o la versión correspondiente a Fabric.
- Si el modelo apunta a archivos locales (CSV), actualizar rutas o regenerar los CSV `_clean` antes de refrescar.

## 8. Flujo de trabajo reproducible (pasos)

1. (Opcional) Consolidar incrementales: `python Datos\unir_datos.py`.
2. Ejecutar `EDAyLoad.ipynb`: revisar/ajustar `DIRECT_BASE`, ejecutar celdas para limpiar y generar `_clean.csv`.
3. Abrir Power BI: `dashboard pbi/dashboard_Surcomotor.pbip` y refrescar (Import o DirectQuery según configuración).

## 9. Buenas prácticas y recomendaciones

- Mantener copias de los CSV originales fuera del control de versiones cuando contengan datos sensibles.
- Evitar commitear archivos binarios o grandes; usar `.gitignore` (ya configurado para partes del proyecto).
- Documentar cualquier cambio en las rutas o en el formato de las tablas maestras.

## 10. Próximos pasos sugeridos

- Añadir un `requirements.txt` o `pyproject.toml` para fijar dependencias.
- Añadir ejemplos de salida (capturas) en `Imagenes/Readme/` para facilitar revisión.
- Automatizar el pipeline (script que ejecute `unir_datos.py`, luego ejecute un runner de Jupyter para generar `_clean.csv`, y finalmente notifique al autor).

## 11. Contacto

Para preguntas, mejoras o reportes de error, abrir un issue en el repositorio o contactarme directamente.

---

Documento generado automáticamente por el asistente. Si quieres, adapto el contenido a un formato / estructura diferente (por ejemplo carpeta `docs/`, Confluence, o README más corto).
