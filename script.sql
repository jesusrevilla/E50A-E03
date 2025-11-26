
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

-- Clientes
INSERT INTO clientes (nombre, correo) VALUES
('Ana Torres', 'ana@example.com'),
('Luis Pérez', 'luis@example.com');

-- Productos
INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200.00),
('Mouse', 25.50),
('Teclado', 45.00);

-- Pedidos
INSERT INTO pedidos (id_cliente, fecha) VALUES
(1, '2025-05-01'),
(2, '2025-05-02');

-- Detalle de pedidos
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES
(1, 1, 1),  -- Ana compra 1 Laptop
(1, 2, 2),  -- Ana compra 2 Mouse
(2, 3, 1);  -- Luis compra 1 Teclado

--EJERCICIOS

--1. VISTA
CREATE VIEW vista_detalle_pedidos AS
SELECT
    p.id_pedido,
    p.fecha,
    c.id_cliente,
    c.nombre AS cliente,
    pr.id_producto,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio::numeric(12,2) AS precio_unitario,
    (pr.precio * dp.cantidad)::numeric(12,2) AS total_linea
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;


SELECT * FROM vista_detalle_pedidos;

--2. PROCEDIMIENTO
CREATE PROCEDURE registrar_pedido(
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

    RAISE NOTICE 'Pedido creado';
END;
$$;

--3. FUNCION
CALL registrar_pedido(1, '2025-05-20', 2, 3);

CREATE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS numeric(14,2)
LANGUAGE sql
AS $$
SELECT COALESCE(SUM(pr.precio * dp.cantidad), 0)::numeric(14,2)
FROM pedidos p
JOIN detalle_pedido dp ON dp.id_pedido = p.id_pedido
JOIN productos pr ON pr.id_producto = dp.id_producto
WHERE p.id_cliente = p_id_cliente;
$$;

SELECT total_gastado_por_cliente(1);

--3 tambien jaja INDEX COMPUESTO
CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);


-- 4. TRIGGERS
-- Tabla de auditoría
CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE FUNCTION fn_auditar_pedido()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, CURRENT_TIMESTAMP);

    RETURN NEW;
END;
$$;


CREATE TRIGGER trg_insert_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_auditar_pedido();

-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

--5. NOSQL  
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

--Extraer todas las acciones de un usuario:
SELECT jsonb_array_elements(historial_actividad)->>'accion' FROM usuarios WHERE id = 1;

--6. GRAFOS

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
(1, 2, 180),  
(2, 3, 350),
(1, 5, 410),
(5, 4, 900),
(3, 4, 700);

 SELECT c2.nombre, r.distancia_km
 FROM rutas r
 JOIN ciudades c2 ON r.id_destino = c2.id
 WHERE r.id_origen = 1;

