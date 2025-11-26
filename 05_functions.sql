-- Función para calcular el total gastado por cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(cliente_id INT)
RETURNS DECIMAL AS $$
DECLARE total DECIMAL;
BEGIN
    SELECT SUM(dp.cantidad * pr.precio)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = cliente_id;

    RETURN COALESCE(total, 0);
END;
$$ LANGUAGE plpgsql;

-- Índice compuesto
CREATE INDEX idx_cliente_producto
ON detalle_pedido (id_pedido, id_producto);
