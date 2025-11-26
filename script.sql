/* ===========================
   VISTA CON JOINS (03)
   =========================== */
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.id_cliente,
    c.nombre AS cliente,
    p.id_pedido,
    p.fecha AS fecha_pedido,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio,
    (dp.cantidad * pr.precio) AS total_linea
FROM clientes c
JOIN pedidos p ON c.id_cliente = p.id_cliente
JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto;

/* ===========================
   PROCEDIMIENTO (04)
   =========================== */
CREATE OR REPLACE PROCEDURE registrar_pedido(
    cliente_id INT,
    fecha_pedido DATE,
    producto_id INT,
    cantidad INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO pedidos (id_cliente, fecha) VALUES (cliente_id, fecha_pedido);
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (currval('pedidos_id_pedido_seq'), producto_id, cantidad);
END;
$$;

/* ===========================
   FUNCIÓN + ÍNDICE (05)
   =========================== */
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(cliente_id INT)
RETURNS DECIMAL AS $$
DECLARE total DECIMAL;
BEGIN
    SELECT SUM(dp.cantidad * pr.precio)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = cliente_id;

    RETURN COALESCE(total, 0);
END;
$$ LANGUAGE plpgsql;

CREATE INDEX idx_cliente_producto
ON detalle_pedido (id_pedido, id_producto);

/* ===========================
   TRIGGER + AUDITORÍA (06)
   =========================== */
CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION registrar_auditoria()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auditoria
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria();

/* ===========================
   JSONB (07)
   =========================== */
CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca":"Dell","ram":"16GB","procesador":"Intel i7"}'),
('Smartphone', '{"marca":"Samsung","pantalla":"6.5 pulgadas","almacenamiento":"128GB"}');

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez','laura@example.com',
 '[{"fecha":"2025-05-01","accion":"inicio_sesion"},
   {"fecha":"2025-05-02","accion":"subio_archivo"}]');

/* ===========================
   GRAFOS (08)
   =========================== */
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);

INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1,2,180), (2,3,350), (1,5,410), (5,4,900), (3,4,700);

