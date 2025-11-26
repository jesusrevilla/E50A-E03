
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    prod.precio AS precio_unitario,
    (dp.cantidad * prod.precio) AS total_linea
FROM
    pedidos pe
JOIN
    clientes c ON pe.id_cliente = c.id_cliente
JOIN
    detalle_pedido dp ON pe.id_pedido = dp.id_pedido
JOIN
    productos prod ON dp.id_producto = prod.id_producto;

-- 2. PROCEDIMIENTO ALMACENADO: registrar_pedido
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
    -- 1. Insertar en la tabla pedidos
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido;

    -- 2. Insertar en la tabla detalle_pedido
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
    
    COMMIT;
END;
$$;

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC AS $$
DECLARE
    total NUMERIC;
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * p.precio), 0.00) INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos p ON dp.id_producto = p.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN total;
END;
$$ LANGUAGE plpgsql;


CREATE INDEX IF NOT EXISTS idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);



CREATE OR REPLACE FUNCTION auditar_nuevo_pedido()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para llamar a la función de auditoría
CREATE OR REPLACE TRIGGER tr_auditar_insert_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION auditar_nuevo_pedido();

CREATE OR REPLACE FUNCTION get_rutas_desde_ciudad(p_ciudad_nombre TEXT)
RETURNS TABLE (
    origen TEXT,
    destino TEXT,
    distancia_km INT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c_origen.nombre AS origen,
        c_destino.nombre AS destino,
        r.distancia_km
    FROM
        rutas r
    JOIN
        ciudades c_origen ON r.id_origen = c_origen.id
    JOIN
        ciudades c_destino ON r.id_destino = c_destino.id
    WHERE
        c_origen.nombre = p_ciudad_nombre;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_acciones_usuario(p_nombre TEXT)
RETURNS TABLE (
    accion TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        jsonb_array_elements(u.historial_actividad)->>'accion' AS accion
    FROM
        usuarios u
    WHERE
        u.nombre = p_nombre;
END;
$$ LANGUAGE plpgsql;
