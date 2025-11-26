--JOINS y Vistas
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    dp.id_detalle, 
    p.nombre, 
    dp.cantidad, 
    c.nombre AS "nombre cliente"
FROM productos p 
INNER JOIN detalle_pedido dp ON p.id_producto = dp.id_producto 
INNER JOIN pedidos ped ON ped.id_pedido = dp.id_pedido 
INNER JOIN clientes c ON c.id_cliente = ped.id_cliente;

--Procedimiento Almacenado
CREATE OR REPLACE PROCEDURE registrar_pedido(id_cliente INT, fecha DATE, id_producto INT, cantidad INT)
AS $$
DECLARE
    v_id_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (id_cliente, fecha)
    RETURNING id_pedido INTO v_id_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, id_producto, cantidad);
END;
$$ LANGUAGE plpgsql;

--función
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(id_clientex INT)
RETURNS DECIMAL(10, 2) AS
$$
DECLARE
    total DECIMAL(10, 2) := 0;
BEGIN
    SELECT SUM(p.precio)
    INTO total
    FROM pedidos ped
    JOIN detalle_pedido dp ON ped.id_pedido = dp.id_pedido
    JOIN productos p ON dp.id_producto = p.id_producto
    WHERE ped.id_cliente = id_clientex;

    RETURN total;
END;
$$ LANGUAGE plpgsql;

--Triggers
CREATE OR REPLACE FUNCTION registrar_pedido_trigger()
RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_pedido ON pedidos;

CREATE TRIGGER trigger_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_pedido_trigger();

--JSON query
CREATE OR REPLACE VIEW vista_historial_pedro AS
SELECT
    ha.value->>'accion' AS accion
FROM usuarios u,
     LATERAL jsonb_array_elements(u.historial_actividad) AS ha
WHERE u.nombre = 'Pedro Ruiz';

-- Gráfos
WITH RECURSIVE grafos AS (
    SELECT 
        c.id AS ciudad_id,
        c.nombre AS ciudad,
        r.id_destino,
        r.distancia_km,
        c.nombre::TEXT AS ruta
    FROM ciudades c
    JOIN rutas r ON c.id = r.id_origen
    WHERE c.id = 1

    UNION ALL

    SELECT
        c2.id AS ciudad_id,
        c2.nombre AS ciudad,
        r2.id_destino,
        r2.distancia_km,
        g.ruta || ' - ' || c2.nombre
    FROM grafos g
    JOIN rutas r2 ON g.id_destino = r2.id_origen
    JOIN ciudades c2 ON r2.id_destino = c2.id
)
SELECT * FROM grafos;
