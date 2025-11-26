CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    pr.precio AS precio_unitario,
    (dp.cantidad * pr.precio) AS total_linea
FROM
    clientes c
JOIN
    pedidos pd ON c.id_cliente = pd.id_cliente
JOIN
    detalle_pedido dp ON pd.id_pedido = dp.id_pedido
JOIN
    productos pr ON dp.id_producto = pr.id_producto;

SELECT * FROM vista_detalle_pedidos;
