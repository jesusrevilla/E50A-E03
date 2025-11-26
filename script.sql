SELECT * FROM vista_detalle_pedidos;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

SELECT total_gastado_por_cliente(1);

INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

SELECT * FROM auditoria_pedidos;

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT c1.nombre as origen, c2.nombre as destino, r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';
