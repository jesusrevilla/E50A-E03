CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    p.precio AS precio_unitario,
    (dp.cantidad * p.precio) AS total_linea,
    pe.fecha AS fecha_compra
FROM 
    detalle_pedido dp
    JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
    JOIN clientes c ON pe.id_cliente = c.id_cliente
    JOIN productos p ON dp.id_producto = p.id_producto;
    
SELECT * FROM vista_detalle_pedidos;
