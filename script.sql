-- 1. joins y vistas
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre as nombre_cliente,
    pr.nombre as nombre_producto,
    dp.cantidad,
    (pr.precio * dp.cantidad) as total_linea
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto;

-- 2. PROCEDIMIENTO ALMACENAD
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
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido;
    
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
    
END;
$$;

-- 3. FUNCIÓN
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(pr.precio * dp.cantidad), 0)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;
    
    RETURN total;
END;
$$;

CREATE INDEX idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);

-- 4. TRIGGERS
CREATE OR REPLACE FUNCTION fn_auditar_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_auditar_pedido
    AFTER INSERT ON pedidos
    FOR EACH ROW
    EXECUTE FUNCTION fn_auditar_pedido();

-- 5. NoSQL
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT nombre, jsonb_array_elements(historial_actividad) as accion
FROM usuarios
WHERE nombre = 'Laura Gómez';

-- 6. GRAFOS 
SELECT 
    c1.nombre as origen,
    c2.nombre as destino,
    r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';
