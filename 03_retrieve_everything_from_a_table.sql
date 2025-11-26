-- 1.Vista
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    (pr.precio * dp.cantidad) AS total_linea
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto;
-- 2. PROCEDIMIENTO registrar_pedido
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE nuevo_id INT;
BEGIN
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_id;

    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad)
    VALUES (nuevo_id, p_id_producto, p_cantidad);
END;
$$;

-- 3. FUNCIÓN total_gastado_por_cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(pr.precio * dp.cantidad), 0)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_cliente;

    RETURN total;
END;
$$;
