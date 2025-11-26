-- Crear vista de detalles de pedidos
CREATE VIEW vista_detalle_pedidos AS
SELECT c.nombre AS cliente,
       p.nombre AS producto,
       dp.cantidad,
       (dp.cantidad * pr.precio) AS total_linea
FROM detalle_pedido dp
JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
JOIN clientes c ON pe.id_cliente = c.id_cliente
JOIN productos p ON dp.id_producto = p.id_producto;

-- Crear índice compuesto para cliente y producto
CREATE INDEX idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);
