--1 Joins y vistas
CREATE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio,
    (dp.cantidad * pr.precio) AS total_linea,
    p.fecha
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;

SELECT * FROM vista_detalle_pedidos;

--2 Procedimiento
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido_id INT;
BEGIN
    -- Insertar en la tabla pedidos
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido_id;

    -- Insertar en la tabla detalle_pedido
    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido_id, p_id_producto, p_cantidad);

    RAISE NOTICE 'Pedido % registrado correctamente.', nuevo_pedido_id;
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

--3 Funcion
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT 
        COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN total;
END;
$$;

SELECT total_gastado_por_cliente(1);

--trigger
CREATE OR REPLACE FUNCTION registrar_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

--Nosql
SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

--grafos
SELECT id FROM ciudades WHERE nombre = 'San Luis Potosí';
