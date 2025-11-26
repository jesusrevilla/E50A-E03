-- Procedimiento para registrar pedido
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_cliente INT,
    p_fecha DATE,
    p_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_pedido INT;
BEGIN
    INSERT INTO pedidos(id_cliente, fecha) VALUES (p_cliente, p_fecha) RETURNING id_pedido INTO new_pedido;
    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad) VALUES (new_pedido, p_producto, p_cantidad);
END;
$$;

-- Función: total gastado por cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_cliente INT)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    total NUMERIC;
BEGIN
    SELECT SUM(d.cantidad * pr.precio) INTO total
    FROM pedidos pd
    JOIN detalle_pedido d ON pd.id_pedido = d.id_pedido
    JOIN productos pr ON d.id_producto = pr.id_producto
    WHERE pd.id_cliente = p_cliente;

    RETURN COALESCE(total, 0);
END;
$$;
