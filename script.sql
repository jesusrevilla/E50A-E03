DROP VIEW IF EXISTS vista_detalle_pedidos;

CREATE VIEW vista_detalle_pedidos AS
SELECT
    p.id_pedido,
    p.fecha,
    c.id_cliente,
    c.nombre      AS nombre_cliente,
    c.correo,
    pr.id_producto,
    pr.nombre     AS nombre_producto,
    pr.precio,
    d.cantidad,
    (pr.precio * d.cantidad) AS total_linea
FROM detalle_pedido d
JOIN pedidos   p  ON d.id_pedido   = p.id_pedido
JOIN clientes  c  ON p.id_cliente  = c.id_cliente
JOIN productos pr ON d.id_producto = pr.id_producto;


DROP PROCEDURE IF EXISTS registrar_pedido;

CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente  INT,
    p_fecha       DATE,
    p_id_producto INT,
    p_cantidad    INT
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



DROP FUNCTION IF EXISTS total_gastado_por_cliente(INT);

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(10,2);
BEGIN
    SELECT
        COALESCE(SUM(pr.precio * d.cantidad), 0)
    INTO v_total
    FROM pedidos p
    JOIN detalle_pedido d ON p.id_pedido = d.id_pedido
    JOIN productos pr      ON d.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;


DROP INDEX IF EXISTS idx_cliente_producto;

CREATE INDEX idx_cliente_producto
ON detalle_pedido (id_pedido, id_producto);

DROP FUNCTION IF EXISTS registrar_auditoria_pedido();

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

-- Trigger
DROP TRIGGER IF EXISTS trg_auditoria_pedidos ON pedidos;

CREATE TRIGGER trg_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();


SELECT *
FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';


SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';


SELECT
    c_origen.nombre  AS ciudad_origen,
    c_destino.nombre AS ciudad_destino,
    r.distancia_km
FROM rutas r
JOIN ciudades c_origen  ON r.id_origen  = c_origen.id
JOIN ciudades c_destino ON r.id_destino = c_destino.id
WHERE c_origen.nombre = 'San Luis Potosí';