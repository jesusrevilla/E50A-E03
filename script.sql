\echo '\tSebastian Heredia Pardo - 175680\n\tEXAMEN 3° PARCIAL - Bases de Datos\n'
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

\echo '\n\t1. Joins y vistas\n'
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

SELECT * FROM vista_detalle_pedidos;

\echo '\n\t2. Procedimiento almacenado\n'
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido_id INT;
BEGIN
    -- Insertar en pedidos
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido_id;

    -- Insertar en detalle_pedido
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido_id, p_id_producto, p_cantidad);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

\echo '\n\t3. Función\n'
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL(10, 2);
BEGIN
    SELECT SUM(dp.cantidad * pr.precio)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN COALESCE(total, 0);
END;
$$;

SELECT total_gastado_por_cliente(1);

CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);


\echo '\n\t4. Disparadores (Triggers)\n'
-- Tabla de auditoría
CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE OR REPLACE FUNCTION registrar_auditoria_pedido()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auditoria_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

-- Insertar nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Consultar auditoría
SELECT * FROM auditoria_pedidos;


\echo '\n\t5. NoSQL\n'
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

SELECT jsonb_array_elements(historial_actividad)->>'accion' AS accion
FROM usuarios
WHERE nombre = 'Laura Gómez';


\echo '\n\t6. Gráfos\n'
-- Nodos: ciudades
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Aristas: rutas entre ciudades
CREATE TABLE rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);

-- Ciudades
INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

-- Rutas (grafo dirigido)
INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),  -- SLP → Querétaro
(2, 3, 350),  -- Querétaro → Guadalajara
(1, 5, 410),  -- SLP → CDMX
(5, 4, 900),  -- CDMX → Monterrey
(3, 4, 700);  -- Guadalajara → Monterrey

SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';

