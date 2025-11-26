CREATE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    d.cantidad,
    pr.precio,
    (d.cantidad * pr.precio) AS total_linea
FROM detalle_pedido d
JOIN pedidos p ON d.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON d.id_producto = pr.id_producto;
