-- Consultar el total gastado por cada cliente
SELECT id_cliente, SUM(precio * cantidad) AS total_gastado
FROM pedidos
JOIN detalle_pedido ON pedidos.id_pedido = detalle_pedido.id_pedido
JOIN productos ON detalle_pedido.id_producto = productos.id_producto
GROUP BY id_cliente;

-- Verificar las rutas entre ciudades
SELECT id_origen, id_destino, distancia_km
FROM rutas
WHERE id_origen = 1;  -- Ver rutas desde San Luis Potosí

