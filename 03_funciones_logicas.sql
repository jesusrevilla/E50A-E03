
-- Parte 1
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio AS precio_unitario,
    (dp.cantidad * pr.precio) AS total_linea,
    p.fecha
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;


-- Parte 2 

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
    -- Insertar pedido y capturar el ID generado
    INSERT INTO pedidos (id_cliente, fecha) 
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido;

    -- Insertar detalle
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) 
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
    
    RAISE NOTICE 'Pedido creado con éxito. ID: %', v_id_pedido;
END;
$$;

-- Parte 3

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO v_total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;
    
    RETURN v_total;
END;
$$;


-- Parte 4

-- Función del trigger
CREATE OR REPLACE FUNCTION funcion_auditoria_pedidos()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$;

-- Disparador
DROP TRIGGER IF EXISTS trg_auditoria_pedido ON pedidos;

CREATE TRIGGER trg_auditoria_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION funcion_auditoria_pedidos();
