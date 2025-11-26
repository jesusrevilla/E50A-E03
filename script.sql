--  Universidad Politécnica de San Luis Potosí
--            07 de Mayo, 2025
--               Base de Datos
--      Christian Alejandro Cárdenas Rucoba

--      Examen Tercer Parcial

--1. Joins y Vistas
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

--Crear una vista con JOINs (vista_detalle_pedidos) Esta vista muestra el detalle de cada pedido, 
--incluyendo el nombre del cliente, producto, cantidad y el total por línea.

CREATE VIEW vista_detalle_pedidos AS
SELECT c.nombre as cliente, p.nombre as producto, d.cantidad, (p.precio*d.cantidad) AS total
FROM clientes c 
JOIN pedidos s ON c.id_cliente = s.id_cliente
JOIN detalle_pedido d ON s.id_pedido = d.id_pedido
JOIN productos p ON d.id_producto = p.id_producto;

--Consultar la vista
SELECT * FROM vista_detalle_pedidos;

--2. Procedimiento almacenado
--Registrar un nuevo pedido Este procedimiento llamado registrar_pedido inserta un nuevo pedido 
--y sus detalles en varias tablas.

CREATE OR REPLACE PROCEDURE registrar_pedido(
    new_id_cliente INT,
    new_fecha DATE,
    new_id_pedido INT,
    new_id_producto INT,
    new_cantidad INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES (new_id_cliente, new_fecha);
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (new_id_pedido, new_id_producto, new_cantidad);
END;
$$;

CALL registrar_pedido (2,'2025-05-21',3,2,1); --numero de cliente, fecha, id de pedido, id de producto, cantidad 
--SELECT * FROM vista_detalle_pedidos;

--3. Función
--Calcula el total gastado por un cliente Esta función devuelve el total gastado por un cliente 
--sumando todos sus pedidos.

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(ch_id_cliente INT)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN (SELECT SUM(p.precio*d.cantidad)
    FROM clientes c 
    JOIN pedidos s ON c.id_cliente = s.id_cliente
    JOIN detalle_pedido d ON s.id_pedido = d.id_pedido
    JOIN productos p ON d.id_producto = p.id_producto
    WHERE c.id_cliente = ch_id_cliente
    );
END;
$$;

SELECT total_gastado_por_cliente(1);

--Y crea un índice compuesto llamado idx_cliente_producto
--CREATE INDEX idx_cliente_producto ON total_gastado_por_cliente(ch_id_cliente);

--4. Disparadores (Triggers)
--Crear un trigger que registre en una tabla de auditoría cada vez
--que se inserte un nuevo pedido, incluyendo el ID del cliente,
--la fecha del pedido y la fecha y hora del registro.

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

CREATE TRIGGER tr_registrar_auditoria_pedido
AFTER INSERT ON auditoria_pedidos
FOR EACH ROW
EXECUTE PROCEDURE registrar_auditoria_pedido();

-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

--5. NoSQL
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

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad IS NOT NULL;

--6. Gráfos
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

SELECT * FROM rutas
WHERE id_origen = 1;
