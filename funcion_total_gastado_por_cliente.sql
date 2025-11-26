CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT SUM(dp.cantidad * pr.precio)
    INTO v_total
    FROM detalle_pedido dp
    JOIN pedidos p ON dp.id_pedido = p.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN COALESCE(v_total, 0);
END;
$$ LANGUAGE plpgsql;
