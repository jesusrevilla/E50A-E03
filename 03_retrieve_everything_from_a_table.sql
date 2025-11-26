CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    d.cantidad,
    pr.precio,
    (d.cantidad * pr.precio) AS subtotal
FROM pedidos p
JOIN clientes c     ON p.id_cliente = c.id_cliente
JOIN detalle_pedido d ON p.id_pedido = d.id_pedido
JOIN productos pr   ON d.id_producto = pr.id_producto;

CREATE OR REPLACE PROCEDURE registrar_pedido(
    _id_cliente INT,
    _fecha DATE,
    _id_producto INT,
    _cantidad INT)
LANGUAGE plpgsql AS $$ DECLARE nuevo_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (_id_cliente, _fecha)
    RETURNING id_pedido INTO nuevo_pedido;

INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES (nuevo_pedido, _id_producto, _cantidad);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);


