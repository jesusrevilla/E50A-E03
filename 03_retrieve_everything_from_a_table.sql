--view
CREATE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    (dp.cantidad * p.precio) AS total_linea
FROM 
    detalle_pedido dp
    JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
    JOIN clientes c ON pe.id_cliente = c.id_cliente
    JOIN productos p ON dp.id_producto = p.id_producto;
SELECT * FROM vista_detalle_pedidos;

--procedure
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_pedido_generado INT; 
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido_generado;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido_generado, p_id_producto, p_cantidad);

    RAISE NOTICE 'Pedido #% registrado correctamente.', v_id_pedido_generado;
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

--function
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * p.precio), 0)
    INTO v_total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos p ON dp.id_producto = p.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;

SELECT total_gastado_por_cliente(1);
-- index
CREATE INDEX idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);

--trigger funcion
CREATE OR REPLACE FUNCTION fn_registrar_auditoria_pedido()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--trigger
CREATE TRIGGER trg_auditoria_nuevo_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_registrar_auditoria_pedido();

--probar TRIGGER
INSERT INTO pedidos (id_cliente, fecha) 
VALUES (1, '2025-05-20');
SELECT * FROM auditoria_pedidos;

SELECT nombre 
FROM usuarios_log 
WHERE historial_actividad @> '[{"accion": "compra"}]';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT 
    nombre,
    elemento->>'fecha' AS fecha,
    elemento->>'accion' AS actividad
FROM 
    usuarios,
    jsonb_array_elements(historial_actividad) AS elemento
WHERE 
    nombre = 'Laura Gómez';
SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    r.distancia_km
FROM 
    rutas r
    JOIN ciudades c1 ON r.id_origen = c1.id
    JOIN ciudades c2 ON r.id_destino = c2.id
WHERE 
    c1.nombre = 'San Luis Potosí';
