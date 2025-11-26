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
    -- Insertar el nuevo pedido
    INSERT INTO pedidos (id_cliente, fecha) 
    VALUES (p_id_cliente, p_fecha) 
    RETURNING id_pedido INTO v_id_pedido;

    -- Insertar detalles del pedido
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) 
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$;
