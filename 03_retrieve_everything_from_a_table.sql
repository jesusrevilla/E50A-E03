-- 1.Vista
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    (pr.precio * dp.cantidad) AS total_linea
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto;

-- 2. PROCEDIMIENTO registrar_pedido
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE nuevo_id INT;
BEGIN
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_id;

    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad)
    VALUES (nuevo_id, p_id_producto, p_cantidad);
END;
$$;

-- 3. FUNCIÓN total_gastado_por_cliente
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(pr.precio * dp.cantidad), 0)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_cliente;

    RETURN total;
END;
$$;

-- 4. ÍNDICE COMPUESTO
CREATE INDEX IF NOT EXISTS idx_cliente_producto
ON detalle_pedido(id_pedido, id_producto);

-- 5. TRIGGER + AUDITORÍA
CREATE TABLE IF NOT EXISTS auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION auditar_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos(id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trigger_auditoria_pedidos ON pedidos;

CREATE TRIGGER trigger_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION auditar_pedido();

-- 6. JSONB (productos_json + usuarios)
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

-- 7. GRAFO (ciudades + rutas)
CREATE TABLE IF NOT EXISTS ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY(id_origen, id_destino)
);

-- 8. RETRIEVE EVERYTHING (para cumplir nombre del archivo)
SELECT * FROM clientes;
SELECT * FROM productos;
SELECT * FROM pedidos;
SELECT * FROM detalle_pedido;
SELECT * FROM productos_json;
SELECT * FROM usuarios;
SELECT * FROM ciudades;
SELECT * FROM rutas;
SELECT * FROM auditoria_pedidos;
