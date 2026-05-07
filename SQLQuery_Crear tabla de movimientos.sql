USE Surcomotor_DB
GO

-- 1. Crear tabla movimientos (si no existe)
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
GO

-- 2. Tabla auxiliar: precios de venta mensuales (por producto y mes)
-- Se toma el primer precio de venta de cada mes (se asume constante durante el mes)
IF OBJECT_ID('tempdb..#PreciosMensualesVenta') IS NOT NULL DROP TABLE #PreciosMensualesVenta;
SELECT 
    Producto,
    YEAR(Fecha) AS Anio,
    MONTH(Fecha) AS Mes,
    MIN(Precio_Venta) AS PrecioVentaMes   -- se podría usar AVG si hubiera variación, pero por diseño es constante
INTO #PreciosMensualesVenta
FROM dbo.tabla_ventas
GROUP BY Producto, YEAR(Fecha), MONTH(Fecha);

-- 3. Tabla auxiliar: costos de compra mensuales
IF OBJECT_ID('tempdb..#CostosMensualesCompra') IS NOT NULL DROP TABLE #CostosMensualesCompra;
SELECT 
    Producto,
    YEAR(Fecha) AS Anio,
    MONTH(Fecha) AS Mes,
    MIN(Precio_Compra) AS CostoCompraMes
INTO #CostosMensualesCompra
FROM dbo.tabla_compras
GROUP BY Producto, YEAR(Fecha), MONTH(Fecha);

-- 4. Función para obtener el último valor mensual no nulo (hasta una fecha)
-- Creamos una vista o usamos OUTER APPLY con lógica de último mes disponible

-- 5. Insertar movimientos de ventas (con costo mensual)
INSERT INTO dbo.movimientos (TipoMovimiento, Fecha, Entidad, Almacen, Producto, Cantidad, CostoUnitario, PrecioUnitario, Monto, Vendedor)
SELECT 
    'Venta',
    v.Fecha,
    v.Cliente,
    v.Almacen,
    v.Producto,
    v.Cantidad_Vendida,
    ISNULL((
        SELECT TOP 1 CostoCompraMes
        FROM #CostosMensualesCompra c
        WHERE c.Producto = v.Producto 
          AND (c.Anio < YEAR(v.Fecha) OR (c.Anio = YEAR(v.Fecha) AND c.Mes <= MONTH(v.Fecha)))
        ORDER BY c.Anio DESC, c.Mes DESC
    ), 0) AS CostoUnitario,
    v.Precio_Venta AS PrecioUnitario,
    v.Monto_Venta,
    v.Vendedor
FROM dbo.tabla_ventas v;
GO

-- 6. Insertar movimientos de compras (con precio de venta mensual)
INSERT INTO dbo.movimientos (TipoMovimiento, Fecha, Entidad, Almacen, Producto, Cantidad, CostoUnitario, PrecioUnitario, Monto, Vendedor)
SELECT 
    'Compra',
    c.Fecha,
    c.Proveedor,
    c.Almacen,
    c.Producto,
    c.Cantidad,
    c.Precio_Compra AS CostoUnitario,
    ISNULL((
        SELECT TOP 1 PrecioVentaMes
        FROM #PreciosMensualesVenta p
        WHERE p.Producto = c.Producto 
          AND (p.Anio < YEAR(c.Fecha) OR (p.Anio = YEAR(c.Fecha) AND p.Mes <= MONTH(c.Fecha)))
        ORDER BY p.Anio DESC, p.Mes DESC
    ), 0) AS PrecioUnitario,
    c.Monto,
    NULL
FROM dbo.tabla_compras c;
GO


-- 7. Insertar movimientos de stock (con tipo real del inventario)
INSERT INTO dbo.movimientos 
(TipoMovimiento, Fecha, Entidad, Almacen, Producto, Cantidad, CostoUnitario, PrecioUnitario, Monto, Vendedor)
SELECT 
    s.Tipo,   -- 'Movimiento de Inventario' o 'Control'
    s.Fecha,
    NULL,
    s.Almacen,
    p.DESCRIPCIÓN,
    s.Cantidad_Stock,
    ISNULL((
        SELECT TOP 1 CostoCompraMes
        FROM #CostosMensualesCompra c
        WHERE c.Producto = p.DESCRIPCIÓN
          AND (c.Anio < YEAR(s.Fecha) OR (c.Anio = YEAR(s.Fecha) AND c.Mes <= MONTH(s.Fecha)))
        ORDER BY c.Anio DESC, c.Mes DESC
    ), 0) AS CostoUnitario,
    ISNULL((
        SELECT TOP 1 PrecioVentaMes
        FROM #PreciosMensualesVenta v
        WHERE v.Producto = p.DESCRIPCIÓN
          AND (v.Anio < YEAR(s.Fecha) OR (v.Anio = YEAR(s.Fecha) AND v.Mes <= MONTH(s.Fecha)))
        ORDER BY v.Anio DESC, v.Mes DESC
    ), 0) AS PrecioUnitario,
    s.Cantidad_Stock * ISNULL((
        SELECT TOP 1 CostoCompraMes
        FROM #CostosMensualesCompra c
        WHERE c.Producto = p.DESCRIPCIÓN
          AND (c.Anio < YEAR(s.Fecha) OR (c.Anio = YEAR(s.Fecha) AND c.Mes <= MONTH(s.Fecha)))
        ORDER BY c.Anio DESC, c.Mes DESC
    ), 0) AS Monto,
    NULL
FROM dbo.tabla_stock_inventario s
INNER JOIN dbo.tabla_productos p ON s.ID_Producto = p.ID_PRODUCTO;
GO

-- 8. Resultado final
SELECT * FROM dbo.movimientos
ORDER BY Fecha, id_movimiento;