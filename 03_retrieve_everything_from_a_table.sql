--1. vista
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    d.cantidad,
    pr.precio,
    (d.cantidad * pr.precio) AS subtotal
FROM pedidos p
JOIN clientes c     ON p.id_cliente = c.id_cliente
JOIN detalle_pedido d ON p.id_pedido = d.id_pedido
JOIN productos pr   ON d.id_producto = pr.id_producto;

--2. ejercicio de procedimiento
CREATE OR REPLACE PROCEDURE registrar_pedido(
    _id_cliente INT,
    _fecha DATE,
    _id_producto INT,
    _cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (_id_cliente, _fecha)
    RETURNING id_pedido INTO nuevo_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido, _id_producto, _cantidad);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

--3. funcion
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(_id INT)
RETURNS NUMERIC AS $$
    SELECT SUM(d.cantidad * p.precio)
    FROM pedidos pe
    JOIN detalle_pedido d ON pe.id_pedido = d.id_pedido
    JOIN productos p      ON d.id_producto = p.id_producto
    WHERE pe.id_cliente = _id;
$$ LANGUAGE SQL;


SELECT total_gastado_por_cliente(1);

--4. trigger
CREATE INDEX idx_cliente_producto
ON detalle_pedido (id_pedido, id_producto);

CREATE OR REPLACE FUNCTION auditoria_nuevo_pedido()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_insert_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION auditoria_nuevo_pedido();

--5. NOSQL
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT jsonb_array_elements(historial_actividad)->>'accion' AS accion
FROM usuarios
WHERE id = 1;

--6. Grafos
SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE r.id_origen = 1;


