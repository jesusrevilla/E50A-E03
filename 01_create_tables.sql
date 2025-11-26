
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre      VARCHAR(100),
    correo      VARCHAR(100)
);

CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre      VARCHAR(100),
    precio      DECIMAL(10, 2)
);

CREATE TABLE pedidos (
    id_pedido  SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha      DATE
);

CREATE TABLE detalle_pedido (
    id_detalle  SERIAL PRIMARY KEY,
    id_pedido   INT REFERENCES pedidos(id_pedido),
    id_producto INT REFERENCES productos(id_producto),
    cantidad    INT
);


CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
    p.id_pedido,
    p.fecha,
    c.nombre  AS nombre_cliente,
    c.correo  AS correo_cliente,
    pr.nombre AS nombre_producto,
    dp.cantidad,
    (dp.cantidad * pr.precio) AS total_linea
FROM pedidos p
JOIN clientes c     ON p.id_cliente = c.id_cliente
JOIN detalle_pedido dp ON dp.id_pedido = p.id_pedido
JOIN productos pr   ON pr.id_producto = dp.id_producto;

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
    -- Insertar en pedidos
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido;

    -- Insertar el detalle
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$;


CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(10,2);
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO v_total
    FROM pedidos p
    JOIN detalle_pedido dp ON dp.id_pedido = p.id_pedido
    JOIN productos pr      ON pr.id_producto = dp.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;


CREATE INDEX idx_cliente_producto
ON pedidos (id_cliente, fecha);


-- Tabla de auditoría
CREATE TABLE auditoria_pedidos (
    id_auditoria   SERIAL PRIMARY KEY,
    id_cliente     INT,
    fecha_pedido   DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Función que usará el trigger
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

-- Trigger que se dispara al insertar un pedido
CREATE TRIGGER trg_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

-- NoSQL con JSONB 

-- Productos con atributos flexibles
CREATE TABLE productos_json (
    id        SERIAL PRIMARY KEY,
    nombre    TEXT,
    atributos JSONB
);

-- Usuarios con historial de actividad (arreglo JSONB)
CREATE TABLE usuarios (
    id                 SERIAL PRIMARY KEY,
    nombre             TEXT,
    correo             TEXT,
    historial_actividad JSONB
);

-- Nodos: ciudades
CREATE TABLE ciudades (
    id     SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Aristas: rutas entre ciudades
CREATE TABLE rutas (
    id_origen    INT REFERENCES ciudades(id),
    id_destino   INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);
