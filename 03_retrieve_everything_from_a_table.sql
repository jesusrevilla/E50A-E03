\set ON_ERROR_STOP on

-- Vista con joins
SELECT * FROM vista_detalle_pedidos ORDER BY id_pedido, producto;

-- Total gastado de ejemplo
SELECT total_gastado_por_cliente(1) AS total_cliente_1;

-- Ejemplo de consulta JSONB: marca Dell
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

-- Ejemplo de consulta JSONB: usuarios con accion inicio_sesion
SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion":"inicio_sesion"}]'::jsonb;

-- Ejemplo grafo: rutas saliendo de San Luis Potosí (id=1)
SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
FROM rutas r
JOIN ciudades c1 ON c1.id = r.id_origen
JOIN ciudades c2 ON c2.id = r.id_destino
WHERE r.id_origen = 1
ORDER BY r.distancia_km;
