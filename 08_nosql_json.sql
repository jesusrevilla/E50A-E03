-- Buscar por marca
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

-- Buscar usuarios que hicieron una acción específica
SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

-- Extraer todas las acciones
SELECT
    nombre,
    jsonb_extract_path_text(historial_actividad, 'accion')
FROM usuarios;
