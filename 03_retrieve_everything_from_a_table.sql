--ejercicio de procedimiento
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

CALL registrar_pedido(1, '2025-05-20', 2, 3);
--
