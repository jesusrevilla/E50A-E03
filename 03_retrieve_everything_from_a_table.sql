-- ----------------------------------------------------
-- 1. JOINS Y VISTAS
-- ----------------------------------------------------

--  Crear una vista con JOINs (vista_detalle_pedidos)
CREATE VIEW vista_detalle_pedidos AS
SELECT
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    p.precio AS precio_unitario,
    (p.precio * dp.cantidad) AS total_linea
FROM
    detalle_pedido dp
JOIN
    pedidos pe ON dp.id_pedido = pe.id_pedido
JOIN
    clientes c ON pe.id_cliente = c.id_cliente
JOIN
    productos p ON dp.id_producto = p.id_producto
ORDER BY
    c.nombre, pe.fecha;

--  Consultar la vista
SELECT '--- 1. VISTA: vista_detalle_pedidos ---' AS Seccion;
SELECT * FROM vista_detalle_pedidos;

-- ----------------------------------------------------
-- 2. PROCEDIMIENTO ALMACENADO
-- ----------------------------------------------------

--  Registrar un nuevo pedido
-- Se crea un procedimiento que inserta el pedido y su primer detalle
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_pedido INT;
BEGIN
    -- 1. Insertar el nuevo pedido en la tabla 'pedidos'
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido; -- Capturar el ID generado

    -- 2. Insertar el detalle del pedido en la tabla 'detalle_pedido'
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);

    -- Nota: Los comandos COMMIT y ROLLBACK han sido eliminados.
    -- PostgreSQL maneja la transacción automáticamente.

EXCEPTION
    WHEN OTHERS THEN
        -- El error hará que la transacción externa (la llamada CALL) se revierta automáticamente.
        RAISE EXCEPTION 'Error al registrar el pedido: %', SQLERRM;
END;
$$;

-- Ejemplo de uso: (Cliente 1, 2025-05-20, Producto 2 (Mouse), 3 unidades)
SELECT '--- 2. PROCEDIMIENTO: registrar_pedido ---' AS Seccion;
CALL registrar_pedido(1, '2025-05-20', 2, 3);
SELECT 'Pedido recién insertado:' AS Nota;
SELECT * FROM pedidos ORDER BY id_pedido DESC LIMIT 1;
SELECT * FROM detalle_pedido ORDER BY id_detalle DESC LIMIT 1;

-- ----------------------------------------------------
-- 3. FUNCIÓN Y ÍNDICE
-- ----------------------------------------------------

--  Calcula el total gastado por un cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE sql
AS $$
    SELECT COALESCE(SUM(dp.cantidad * pro.precio), 0.00)
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pro ON dp.id_producto = pro.id_producto
    WHERE pe.id_cliente = p_id_cliente;
$$;

-- Crear un índice compuesto llamado idx_cliente_producto
CREATE INDEX idx_cliente_producto ON detalle_pedido (id_producto, cantidad);

-- Ejemplo de uso
SELECT '--- 3. FUNCIÓN: total_gastado_por_cliente ---' AS Seccion;
-- Cliente 1 (Ana Torres): (1 * 1200.00) + (2 * 25.50) + (3 * 25.50 [pedido recién insertado]) = 1200 + 51 + 76.50 = 1327.50
SELECT
    c.nombre AS cliente,
    total_gastado_por_cliente(c.id_cliente) AS total_gastado
FROM
    clientes c
WHERE
    c.id_cliente = 1;
-- Cliente 2 (Luis Pérez): (1 * 45.00) = 45.00
SELECT
    c.nombre AS cliente,
    total_gastado_por_cliente(c.id_cliente) AS total_gastado
FROM
    clientes c
WHERE
    c.id_cliente = 2;

-- ----------------------------------------------------
-- 4. DISPARADORES (TRIGGERS)
-- ----------------------------------------------------

--  Crear la función que será llamada por el trigger
CREATE OR REPLACE FUNCTION log_nuevo_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insertar un registro en la tabla de auditoría con los datos del nuevo pedido (NEW)
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);

    -- El trigger debe devolver NEW o NULL
    RETURN NEW;
END;
$$;

--  3. Crear el trigger
CREATE TRIGGER tr_registrar_auditoria
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION log_nuevo_pedido();

--  4. Probar el trigger
SELECT '--- 4. TRIGGERS: Prueba de Auditoría ---' AS Seccion;
-- Insertar un nuevo pedido (ID de cliente 1, fecha 2025-05-20)
-- Este INSERT debería disparar el trigger
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-25');

-- Verificar la auditoría
SELECT 'Registro en auditoria_pedidos después del INSERT:' AS Nota;
SELECT id_cliente, fecha_pedido, fecha_registro
FROM auditoria_pedidos
ORDER BY id_auditoria DESC LIMIT 1;

-- ----------------------------------------------------
-- 5. NoSQL (JSONB en PostgreSQL)
-- ----------------------------------------------------
--  Consultar productos con un atributo específico (marca = Dell)
SELECT '--- 5. NoSQL/JSONB: Consultar Laptop Dell ---' AS Seccion;
SELECT id, nombre, atributos
FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

--  Objetivo: Registro de usuarios con historial de actividad (JSONB)
--  Consultar usuarios que realizaron una acción específica (inicio_sesion)
SELECT '--- 5. NoSQL/JSONB: Usuarios con "inicio_sesion" ---' AS Seccion;
SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';


--  Extraer todas las acciones de un usuario
SELECT '--- 5. NoSQL/JSONB: Extraer todas las acciones de Laura Gómez ---' AS Seccion;
-- Usamos jsonb_array_elements para expandir el arreglo en filas
SELECT
    nombre,
    (actividad ->> 'fecha') AS fecha,
    (actividad ->> 'accion') AS accion_realizada
FROM
    usuarios,
    jsonb_array_elements(historial_actividad) AS actividad
WHERE
    nombre = 'Laura Gómez';

-- ----------------------------------------------------
-- 6. GRAFOS (Modelado Relacional)
-- ----------------------------------------------------
--  3. Consulta útil: Ver todas las rutas desde San Luis Potosí
SELECT '--- 6. GRAFOS: Rutas desde San Luis Potosí ---' AS Seccion;
SELECT
    c_origen.nombre AS ciudad_origen,
    c_destino.nombre AS ciudad_destino,
    r.distancia_km
FROM
    rutas r
JOIN
    ciudades c_origen ON r.id_origen = c_origen.id
JOIN
    ciudades c_destino ON r.id_destino = c_destino.id
WHERE
    c_origen.nombre = 'San Luis Potosí';
