--------------- Ejercicios -----------------------
-- Yazmn Guerrero Guevara  182483

--VISTA:  vista_detalle_pedidos

CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    (dp.cantidad * pr.precio) AS total_linea
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;

--PROCEDURE registrar_pedido
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT)
LANGUAGE plpgsql AS $$
DECLARE
    nuevo_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha) VALUES (p_id_cliente, p_fecha) RETURNING id_pedido INTO nuevo_pedido;
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES (nuevo_pedido, p_id_producto, p_cantidad);
END;
$$;

--FUNCIÓN: total_gastado_por_cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_cliente INT)
RETURNS DECIMAL AS $$
DECLARE
    total DECIMAL;
BEGIN
    SELECT SUM(dp.cantidad * pr.precio)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_cliente;

    RETURN COALESCE(total, 0);
END;
$$ LANGUAGE plpgsql;

--CREAR ÍNDICE 
CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);

--TRIGGER DE AUDITORÍA
CREATE OR REPLACE FUNCTION registrar_auditoria() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditoria_pedidos AFTER INSERT ON pedidos
FOR EACH ROW EXECUTE FUNCTION registrar_auditoria();

--CONSULTAS QUE SE PIDEN EN EL README
SELECT * FROM vista_detalle_pedidos;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

SELECT total_gastado_por_cliente(1);

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT jsonb_array_elements(historial_actividad)->>'accion' FROM usuarios WHERE id = 1;

SELECT * FROM rutas WHERE id_origen = 1;

