-- Ejercicio 1
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    d.cantidad,
    (d.cantidad * p.precio) AS total_por_linea
FROM 
    detalle_pedido d
JOIN 
    pedidos pe ON d.id_pedido = pe.id_pedido
JOIN 
    clientes c ON pe.id_cliente = c.id_cliente
JOIN 
    productos p ON d.id_producto = p.id_producto;

-- Ejercicio 2
