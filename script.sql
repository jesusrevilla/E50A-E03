-- Consultar vista de pedidos
SELECT * FROM vista_detalle_pedidos;

-- Consultar auditoría
SELECT * FROM auditoria_pedidos;

-- Consultar productos JSON
SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell';

-- Consultar usuarios con acción específica
SELECT nombre FROM usuarios WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

-- Consultar rutas desde San Luis Potosí
WITH RECURSIVE conexiones AS (
    SELECT id_origen, id_destino, distancia_km FROM rutas WHERE id_origen = 1
    UNION ALL
    SELECT r.id_origen, r.id_destino, r.distancia_km
    FROM rutas r
    INNER JOIN conexiones c ON r.id_origen = c.id_destino
)
SELECT * FROM conexiones;

