SELECT 'Clientes' as tabla, COUNT(*) as cantidad FROM clientes
UNION ALL
SELECT 'Productos', COUNT(*) FROM productos
UNION ALL
SELECT 'Pedidos', COUNT(*) FROM pedidos
UNION ALL
SELECT 'Detalle Pedido', COUNT(*) FROM detalle_pedido
UNION ALL
SELECT 'Auditoría Pedidos', COUNT(*) FROM auditoria_pedidos
UNION ALL
SELECT 'Productos JSON', COUNT(*) FROM productos_json
UNION ALL
SELECT 'Usuarios', COUNT(*) FROM usuarios
UNION ALL
SELECT 'Ciudades', COUNT(*) FROM ciudades
UNION ALL
SELECT 'Rutas', COUNT(*) FROM rutas;
