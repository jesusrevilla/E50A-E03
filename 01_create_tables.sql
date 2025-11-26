SELECT 'CREATE DATABASE exercises'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'exercises')
\gexec;


-- =========================================================
-- 1) Crear TODO en la DB actual (test_db)
-- =========================================================
BEGIN;

-- Limpieza (ordenado por dependencias)
DROP VIEW IF EXISTS vista_detalle_pedidos CASCADE;

DROP TRIGGER IF EXISTS trg_auditar_pedido ON pedidos;
DROP FUNCTION IF EXISTS fn_auditar_pedido();

DROP PROCEDURE IF EXISTS registrar_pedido(INT, DATE, INT, INT);
DROP FUNCTION IF EXISTS total_gastado_por_cliente(INT);

DROP TABLE IF EXISTS rutas CASCADE;
DROP TABLE IF EXISTS ciudades CASCADE;

DROP TABLE IF EXISTS auditoria_pedidos CASCADE;
DROP TABLE IF EXISTS detalle_pedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

DROP TABLE IF EXISTS productos_json CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- -----------------------------
-- Tablas relacionales base
-- -----------------------------
CREATE TABLE clientes (
  id_cliente SERIAL PRIMARY KEY,
  nombre     VARCHAR(100) NOT NULL,
  correo     VARCHAR(100) NOT NULL
);

CREATE TABLE productos (
  id_producto SERIAL PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  precio      NUMERIC(10,2) NOT NULL CHECK (precio >= 0)
);

CREATE TABLE pedidos (
  id_pedido  SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL REFERENCES clientes(id_cliente),
  fecha      DATE NOT NULL
);

CREATE TABLE detalle_pedido (
  id_detalle  SERIAL PRIMARY KEY,
  id_pedido   INT NOT NULL REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
  id_producto INT NOT NULL REFERENCES productos(id_producto),
  cantidad    INT NOT NULL CHECK (cantidad > 0)
);

-- -----------------------------
-- 1) Vista con JOINs
-- -----------------------------
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
  pe.id_pedido,
  c.nombre  AS cliente,
  pr.nombre AS producto,
  dp.cantidad,
  (dp.cantidad * pr.precio)::NUMERIC(12,2) AS total_linea,
  pe.fecha
FROM pedidos pe
JOIN clientes c        ON c.id_cliente = pe.id_cliente
JOIN detalle_pedido dp ON dp.id_pedido = pe.id_pedido
JOIN productos pr      ON pr.id_producto = dp.id_producto;

-- -----------------------------
-- 2) Procedimiento almacenado
-- -----------------------------
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
  IF p_cantidad IS NULL OR p_cantidad <= 0 THEN
    RAISE EXCEPTION 'cantidad debe ser > 0';
  END IF;

  INSERT INTO pedidos (id_cliente, fecha)
  VALUES (p_id_cliente, p_fecha)
  RETURNING id_pedido INTO v_id_pedido;

  INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
  VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$;

-- -----------------------------
-- 3) Función total gastado
-- -----------------------------
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC(12,2)
LANGUAGE sql
AS $$
  SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)::NUMERIC(12,2)
  FROM pedidos pe
  JOIN detalle_pedido dp ON dp.id_pedido = pe.id_pedido
  JOIN productos pr      ON pr.id_producto = dp.id_producto
  WHERE pe.id_cliente = p_id_cliente;
$$;

-- Índice compuesto solicitado (validan el nombre)
CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);

-- -----------------------------
-- 4) Trigger de auditoría
-- -----------------------------
CREATE TABLE auditoria_pedidos (
  id_auditoria   SERIAL PRIMARY KEY,
  id_cliente     INT NOT NULL,
  fecha_pedido   DATE NOT NULL,
  fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_auditar_pedido()
RETURNS trigger
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

-- -----------------------------
-- 5) NoSQL con JSONB
-- -----------------------------
CREATE TABLE productos_json (
  id        SERIAL PRIMARY KEY,
  nombre    TEXT NOT NULL,
  atributos JSONB NOT NULL
);

CREATE TABLE usuarios (
  id                 SERIAL PRIMARY KEY,
  nombre             TEXT NOT NULL,
  correo             TEXT NOT NULL,
  historial_actividad JSONB NOT NULL
);

-- -----------------------------
-- 6) Grafos (ciudades / rutas)
-- -----------------------------
CREATE TABLE ciudades (
  id     SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL
);

CREATE TABLE rutas (
  id_origen    INT NOT NULL REFERENCES ciudades(id),
  id_destino   INT NOT NULL REFERENCES ciudades(id),
  distancia_km INT NOT NULL CHECK (distancia_km > 0),
  PRIMARY KEY (id_origen, id_destino)
);

COMMIT;

-- =========================================================
-- 2) Repetir TODO en la DB "exercises" (porque tu workflow inserta ahí)
-- =========================================================
\connect exercises

BEGIN;

DROP VIEW IF EXISTS vista_detalle_pedidos CASCADE;

DROP TRIGGER IF EXISTS trg_auditar_pedido ON pedidos;
DROP FUNCTION IF EXISTS fn_auditar_pedido();

DROP PROCEDURE IF EXISTS registrar_pedido(INT, DATE, INT, INT);
DROP FUNCTION IF EXISTS total_gastado_por_cliente(INT);

DROP TABLE IF EXISTS rutas CASCADE;
DROP TABLE IF EXISTS ciudades CASCADE;

DROP TABLE IF EXISTS auditoria_pedidos CASCADE;
DROP TABLE IF EXISTS detalle_pedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

DROP TABLE IF EXISTS productos_json CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

CREATE TABLE clientes (
  id_cliente SERIAL PRIMARY KEY,
  nombre     VARCHAR(100) NOT NULL,
  correo     VARCHAR(100) NOT NULL
);

CREATE TABLE productos (
  id_producto SERIAL PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  precio      NUMERIC(10,2) NOT NULL CHECK (precio >= 0)
);

CREATE TABLE pedidos (
  id_pedido  SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL REFERENCES clientes(id_cliente),
  fecha      DATE NOT NULL
);

CREATE TABLE detalle_pedido (
  id_detalle  SERIAL PRIMARY KEY,
  id_pedido   INT NOT NULL REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
  id_producto INT NOT NULL REFERENCES productos(id_producto),
  cantidad    INT NOT NULL CHECK (cantidad > 0)
);

CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
  pe.id_pedido,
  c.nombre  AS cliente,
  pr.nombre AS producto,
  dp.cantidad,
  (dp.cantidad * pr.precio)::NUMERIC(12,2) AS total_linea,
  pe.fecha
FROM pedidos pe
JOIN clientes c        ON c.id_cliente = pe.id_cliente
JOIN detalle_pedido dp ON dp.id_pedido = pe.id_pedido
JOIN productos pr      ON pr.id_producto = dp.id_producto;

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
  IF p_cantidad IS NULL OR p_cantidad <= 0 THEN
    RAISE EXCEPTION 'cantidad debe ser > 0';
  END IF;

  INSERT INTO pedidos (id_cliente, fecha)
  VALUES (p_id_cliente, p_fecha)
  RETURNING id_pedido INTO v_id_pedido;

  INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
  VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$;

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC(12,2)
LANGUAGE sql
AS $$
  SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)::NUMERIC(12,2)
  FROM pedidos pe
  JOIN detalle_pedido dp ON dp.id_pedido = pe.id_pedido
  JOIN productos pr      ON pr.id_producto = dp.id_producto
  WHERE pe.id_cliente = p_id_cliente;
$$;

CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);

CREATE TABLE auditoria_pedidos (
  id_auditoria   SERIAL PRIMARY KEY,
  id_cliente     INT NOT NULL,
  fecha_pedido   DATE NOT NULL,
  fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_auditar_pedido()
RETURNS trigger
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

CREATE TABLE productos_json (
  id        SERIAL PRIMARY KEY,
  nombre    TEXT NOT NULL,
  atributos JSONB NOT NULL
);

CREATE TABLE usuarios (
  id                 SERIAL PRIMARY KEY,
  nombre             TEXT NOT NULL,
  correo             TEXT NOT NULL,
  historial_actividad JSONB NOT NULL
);

CREATE TABLE ciudades (
  id     SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL
);

CREATE TABLE rutas (
  id_origen    INT NOT NULL REFERENCES ciudades(id),
  id_destino   INT NOT NULL REFERENCES ciudades(id),
  distancia_km INT NOT NULL CHECK (distancia_km > 0),
  PRIMARY KEY (id_origen, id_destino)
);

COMMIT;

