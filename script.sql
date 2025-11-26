
-- script.sql
-- Vista, procedimiento, función, índice, trigger y consultas de prueba

-- 1) VISTA con JOINs
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    (pr.precio * dp.cantidad) AS total_linea
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;

-- Consulta de la vista (ejemplo)
-- SELECT * FROM vista_detalle_pedidos;

-- 2) PROCEDIMIENTO: registrar_pedido
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido INT;
BEGIN
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido;

    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido, p_id_producto, p_cantidad);
END;
$$;

-- Ejemplo:
-- CALL registrar_pedido(1, '2025-05-20', 2, 3);

-- 3) FUNCIÓN: total_gastado_por_cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL := 0;
BEGIN
    SELECT SUM(pr.precio * dp.cantidad)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN COALESCE(total, 0);
END;
$$;

-- Ejemplo:
-- SELECT total_gastado_por_cliente(1);

-- Índice compuesto
CREATE INDEX IF NOT EXISTS idx_cliente_producto
ON detalle_pedido(id_pedido, id_producto);

-- 4) TRIGGER y función de auditoría
CREATE OR REPLACE FUNCTION registrar_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos(id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trigger_auditoria_pedidos ON pedidos;

CREATE TRIGGER trigger_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

-- Probar trigger:
-- INSERT INTO pedidos(id_cliente, fecha) VALUES (1, '2025-05-20');
-- SELECT * FROM auditoria_pedidos;

-- 5) Consultas JSONB / NoSQL
-- Buscar productos con marca Dell
-- SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell';

-- Buscar usuarios que iniciaron sesión
-- SELECT nombre, correo FROM usuarios WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

-- Extraer acciones de un usuario
-- SELECT jsonb_array_elements(historial_actividad)->>'accion' AS accion FROM usuarios WHERE id = 1;

-- 6) Consulta de grafo: rutas desde San Luis Potosí
-- SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
-- FROM rutas r
-- JOIN ciudades c1 ON r.id_origen = c1.id
-- JOIN ciudades c2 ON r.id_destino = c2.id
-- WHERE c1.nombre = 'San Luis Potosí';
