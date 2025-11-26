CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS cliente,
    p.nombre AS producto,
    dp.cantidad,
    (dp.cantidad * p.precio) AS total_linea
FROM detalle_pedido dp
JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
JOIN clientes c ON pe.id_cliente = c.id_cliente
JOIN productos p ON dp.id_producto = p.id_producto;

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
    INSERT INTO pedidos(id_cliente, fecha) 
    VALUES (p_id_cliente, p_fecha) 
    RETURNING id_pedido INTO v_id_pedido;

    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad) 
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$;

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

CREATE INDEX IF NOT EXISTS idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);

CREATE TABLE IF NOT EXISTS auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_auditoria_pedidos()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos(id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_auditoria_pedidos();

CREATE TABLE IF NOT EXISTS productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}'),
('Smartphone', '{"marca": "Samsung", "pantalla": "6.5 pulgadas", "almacenamiento": "128GB"}'),
('Tablet', '{"marca": "Apple", "modelo": "iPad Air", "color": "gris"}');

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez', 'laura@example.com', '[{"fecha": "2025-05-01", "accion": "inicio_sesion"}, {"fecha": "2025-05-02", "accion": "subio_archivo"}, {"fecha": "2025-05-03", "accion": "cerró_sesion"}]'),
('Pedro Ruiz', 'pedro@example.com', '[{"fecha": "2025-05-01", "accion": "inicio_sesion"}, {"fecha": "2025-05-04", "accion": "comentó_publicación"}]');

CREATE TABLE IF NOT EXISTS ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);

INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180), (2, 3, 350), (1, 5, 410), (5, 4, 900), (3, 4, 700);
