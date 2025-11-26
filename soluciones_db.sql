-- 1. Joins y Vistas

CREATE VIEW vista_detalle_pedidos AS
SELECT
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    (dp.cantidad * prod.precio) AS total_linea
FROM
    detalle_pedido dp
JOIN
    pedidos p ON dp.id_pedido = p.id_pedido
JOIN
    clientes c ON p.id_cliente = c.id_cliente
JOIN
    productos prod ON dp.id_producto = prod.id_producto;

SELECT * FROM vista_detalle_pedidos;

---
-- 2. Procedimiento almacenado

CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

---
-- 3. Función

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(
    p_id_cliente INT
)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC;
BEGIN
    SELECT
        COALESCE(SUM(dp.cantidad * p.precio), 0) INTO v_total
    FROM
        pedidos pe
    JOIN
        detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN
        productos p ON dp.id_producto = p.id_producto
    WHERE
        pe.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;

SELECT total_gastado_por_cliente(1);

CREATE INDEX idx_cliente_producto ON detalle_pedido (id_producto, id_pedido);

---
-- 4. Disparadores (Triggers)

CREATE OR REPLACE FUNCTION auditar_nuevo_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_auditar_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION auditar_nuevo_pedido();

INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

SELECT * FROM auditoria_pedidos;

---
-- 5. NoSQL (JSONB)

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT
    nombre,
    jsonb_array_elements(historial_actividad) ->> 'accion' AS accion
FROM
    usuarios
WHERE
    nombre = 'Laura Gómez';

---
-- 6. Grafos

SELECT
    c_origen.nombre AS origen,
    c_destino.nombre AS destino,
    r.distancia_km
FROM
    rutas r
JOIN
    ciudades c_origen ON r.id_origen = c_origen.id
JOIN
    ciudades c_destino ON r.id_destino = c_destino.id
WHERE
    c_origen.nombre = 'San Luis Potosí';
