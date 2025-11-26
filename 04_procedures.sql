-- Procedimiento para registrar un pedido
CREATE OR REPLACE PROCEDURE registrar_pedido(
    cliente_id INT,
    fecha_pedido DATE,
    producto_id INT,
    cantidad INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO pedidos (id_cliente, fecha) VALUES (cliente_id, fecha_pedido);
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (currval('pedidos_id_pedido_seq'), producto_id, cantidad);
END;
$$;
