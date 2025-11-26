-- Vista que muestra el detalle de pedidos con cliente, producto, cantidad y total por línea
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.id_cliente,
    c.nombre AS cliente,
    p.id_pedido,
    p.fecha AS fecha_pedido,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio,
    (dp.cantidad * pr.precio) AS total_linea
FROM clientes c
JOIN pedidos p 
    ON c.id_cliente = p.id_cliente
JOIN detalle_pedido dp 
    ON p.id_pedido = dp.id_pedido
JOIN productos pr 
    ON dp.id_producto = pr.id_producto;
