CREATE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio,
    (dp.cantidad * pr.precio) AS total_linea
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;

SELECT * FROM vista_detalle_pedidos;

-- 02 procedimiento  alamacenado
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

    RAISE NOTICE 'Pedido registrado: %, Cliente: %, Producto: %, Cantidad: %',
        v_id_pedido, p_id_cliente, p_id_producto, p_cantidad;
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);


-- 03 funcion
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO v_total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;


SELECT total_gastado_por_cliente(1);


-- 04 Disparadores (Triggers)

CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE OR REPLACE FUNCTION fn_auditar_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);

    RETURN NEW;
END;
$$;


CREATE TRIGGER trg_auditar_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_auditar_pedido();

INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

SELECT * FROM auditoria_pedidos;

-- 05 NoSQL

CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}'),
('Smartphone', '{"marca": "Samsung", "pantalla": "6.5 pulgadas", "almacenamiento": "128GB"}'),
('Tablet', '{"marca": "Apple", "modelo": "iPad Air", "color": "gris"}');

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez', 'laura@example.com', '[
    {"fecha": "2025-05-01", "accion": "inicio_sesion"},
    {"fecha": "2025-05-02", "accion": "subio_archivo"},
    {"fecha": "2025-05-03", "accion": "cerró_sesion"}
]'),
('Pedro Ruiz', 'pedro@example.com', '[
    {"fecha": "2025-05-01", "accion": "inicio_sesion"},
    {"fecha": "2025-05-04", "accion": "comentó_publicación"}
]');

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT 
    u.nombre,
    actividad ->> 'accion' AS accion,
    actividad ->> 'fecha' AS fecha
FROM usuarios u,
     jsonb_array_elements(u.historial_actividad) AS actividad
WHERE u.nombre = 'Laura Gómez';

SELECT 
    u.nombre,
    u.correo,
    actividad ->> 'accion' AS accion,
    actividad ->> 'fecha' AS fecha
FROM usuarios u,
     jsonb_array_elements(u.historial_actividad) AS actividad;
