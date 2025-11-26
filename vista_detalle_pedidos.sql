CREATE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS cliente,
    p.nombre AS producto,
    dp.cantidad,
    (dp.cantidad * pr.precio) AS total
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;
