-- Vista detalle de pedidos
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT pd.id_pedido, c.nombre AS cliente, pr.nombre AS producto, d.cantidad, (d.cantidad*pr.precio) AS total_linea
FROM detalle_pedido d
JOIN pedidos pd ON d.id_pedido = pd.id_pedido
JOIN clientes c ON pd.id_cliente = c.id_cliente
JOIN productos pr ON d.id_producto = pr.id_producto;

-- Índice compuesto cliente-producto
CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);
