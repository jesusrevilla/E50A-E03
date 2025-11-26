
-- ===============================================
-- 1. Vista: vista_detalle_pedidos
-- ===============================================

CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio,
    (dp.cantidad * pr.precio) AS total_linea,
    p.fecha
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;

-- ===============================================
-- 2. Procedimiento: registrar_pedido
-- ===============================================

CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido_id INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido_id;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido_id, p_id_producto, p_cantidad);

    RAISE NOTICE 'Pedido % registrado correctamente.', nuevo_pedido_id;
END $$;

-- ===============================================
-- 3. Función: total_gastado_por_cliente
-- ===============================================

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT 
        COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN total;
END $$;

-- ===============================================
-- 4. Trigger: auditoría de pedidos
-- ===============================================

CREATE OR REPLACE FUNCTION fn_registrar_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);

    RETURN NEW;
END $$;

CREATE OR REPLACE TRIGGER trg_auditar_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_registrar_auditoria_pedido();

-- ===============================================
-- 5. NoSQL JSONB queries (definiciones)
-- (Solo se dejan listas para usar en tests)
-- ===============================================

-- Consulta productos por atributo 'marca'
-- SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell';

-- Consulta usuarios con accion 'inicio_sesion'
-- SELECT nombre, correo FROM usuarios 
-- WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

-- Extraer acciones de un usuario
-- SELECT (elem->>'fecha'), (elem->>'accion')
-- FROM usuarios, jsonb_array_elements(historial_actividad) AS elem
-- WHERE id = 1;

-- ===============================================
-- 6. Grafos - consulta rutas desde SLP
-- ===============================================

-- SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km 
-- FROM rutas r 
-- JOIN ciudades c1 ON r.id_origen = c1.id 
-- JOIN ciudades c2 ON r.id_destino = c2.id 
-- WHERE c1.nombre = 'San Luis Potosí';


