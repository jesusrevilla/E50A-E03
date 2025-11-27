-- ============================
-- CREACIÓN DE TABLAS PRINCIPALES
-- ============================

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100)
);

CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10, 2)
);

CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha DATE
);

CREATE TABLE detalle_pedido (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES pedidos(id_pedido),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT
);

-- ============================
-- VISTA: vista_detalle_pedidos
-- ============================

CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    d.cantidad,
    (d.cantidad * pr.precio) AS total_linea
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN detalle_pedido d ON p.id_pedido = d.id_pedido
JOIN productos pr ON d.id_producto = pr.id_producto;

-- ============================
-- PROCEDIMIENTO registrar_pedido
-- ============================

CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE 
    nuevo_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido, p_id_producto, p_cantidad);
END;
$$;

-- ============================
-- FUNCIÓN total_gastado_por_cliente
-- ============================

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE total DECIMAL(10,2);
BEGIN
    SELECT SUM(d.cantidad * pr.precio)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido d ON pe.id_pedido = d.id_pedido
    JOIN productos pr ON d.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_id;

    RETURN COALESCE(total, 0);
END;
$$;

-- ============================
-- ÍNDICE COMPUESTO
-- ============================

CREATE INDEX idx_cliente_producto
ON detalle_pedido (id_pedido, id_producto);

-- ============================
-- TABLA AUDITORÍA
-- ============================

CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================
-- FUNCIÓN DEL TRIGGER
-- ============================

CREATE OR REPLACE FUNCTION log_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

-- ============================
-- TRIGGER
-- ============================

CREATE TRIGGER trg_log_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION log_pedido();

-- ============================
-- JSONB
-- ============================

CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

-- ============================
-- GRAFO
-- ============================

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

