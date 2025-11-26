

-- 1. TABLAS BASE
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


-- 2. VISTA (vista_detalle_pedidos)
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    (pr.precio * dp.cantidad) AS total_linea
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;


-- 3. PROCEDIMIENTO registrar_pedido()
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
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES(p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido;

    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad)
    VALUES(nuevo_pedido, p_id_producto, p_cantidad);
END;
$$;


-- 4. FUNCIÓN total_gastado_por_cliente()
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL := 0;
BEGIN
    SELECT SUM(pr.precio * dp.cantidad)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN COALESCE(total, 0);
END;
$$;


-- 5. ÍNDICE COMPUESTO
CREATE INDEX idx_cliente_producto
ON detalle_pedido(id_pedido, id_producto);


-- 6. TABLA DE AUDITORÍA
CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 7. FUNCIÓN DEL TRIGGER
CREATE OR REPLACE FUNCTION registrar_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos(id_cliente, fecha_pedido)
    VALUES(NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;


-- 8. TRIGGER
CREATE TRIGGER trigger_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();


-- 9. TABLAS NOSQL (JSONB)
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


-- 10. GRAFOS — CIUDADES Y RUTAS
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

