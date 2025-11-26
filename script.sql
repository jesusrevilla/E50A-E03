-- 1. Procedimiento Almacenado
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

    COMMIT;
END;
$$;

--  2. Función
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE sql
AS $$
SELECT
    COALESCE(SUM(dp.cantidad * pr.precio), 0.00)
FROM
    pedidos p
JOIN
    detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN
    productos pr ON dp.id_producto = pr.id_producto
WHERE
    p.id_cliente = p_id_cliente;
$$;

--3. Vista
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
    c.nombre AS nombre_cliente,
    p.fecha AS fecha_pedido,
    pr.nombre AS nombre_producto,
    dp.cantidad,
    pr.precio AS precio_unitario,
    (dp.cantidad * pr.precio) AS total_linea
FROM
    clientes c
JOIN
    pedidos p ON c.id_cliente = p.id_cliente
JOIN
    detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN
    productos pr ON dp.id_producto = pr.id_producto;

-- 4. Trigger (Función y Trigger)
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

CREATE OR REPLACE TRIGGER trg_auditoria_nuevo_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

--  5. Crear el índice compuesto
CREATE INDEX IF NOT EXISTS idx_pedido_producto ON detalle_pedido (id_pedido, id_producto);

--  6. Tablas JSONB (Si no se incluyeron en 01_create_tables.sql)
CREATE TABLE IF NOT EXISTS productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}'),
('Smartphone', '{"marca": "Samsung", "pantalla": "6.5 pulgadas", "almacenamiento": "128GB"}'),
('Tablet', '{"marca": "Apple", "modelo": "iPad Air", "color": "gris"}');

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez', 'laura@example.com', '[{"fecha": "2025-05-01", "accion": "inicio_sesion"}, {"fecha": "2025-05-02", "accion": "subio_archivo"}]'),
('Pedro Ruiz', 'pedro@example.com', '[{"fecha": "2025-05-01", "accion": "inicio_sesion"}, {"fecha": "2025-05-04", "accion": "comentó_publicación"}]');
