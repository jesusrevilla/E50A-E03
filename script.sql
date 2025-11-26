CREATE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    dp.cantidad * p.precio AS total_linea
FROM detalle_pedido dp
JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
JOIN clientes c ON ped.id_cliente = c.id_cliente
JOIN productos p ON dp.id_producto = p.id_producto;

