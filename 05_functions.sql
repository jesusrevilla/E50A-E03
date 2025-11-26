CREATE OR REPLACE FUNCTION total_gastado_por_cliente(id INT)
RETURNS DECIMAL
LANGUAGE SQL
AS $$
    SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = id;
$$;
