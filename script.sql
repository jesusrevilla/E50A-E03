-- Crear una vista con JOINs (vista_detalle_pedidos) Esta vista muestra el 
-- detalle de cada pedido, incluyendo el nombre del cliente, producto, cantidad y el total por línea.
--Create view
CREATE VIEW vista_detalle_pedidos AS
SELECT c.nombre, p.id_producto, d.cantidad, p.precio * d.cantidad AS total
FROM detalle_pedido d
JOIN productos p ON d.id_producto = p.id_producto
JOIN pedidos pe ON d.id_pedido = pe.id_pedido
JOIN clientes c ON pe.id_cliente = c.id_cliente;

SELECT * FROM vista_detalle_pedidos;

-- Registrar un nuevo pedido Este procedimiento llamado registrar_pedido 
-- inserta un nuevo pedido y sus detalles en varias tablas.
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,    -- ID del cliente
    p_fecha DATE,        -- Fecha del pedido
    p_id_producto INT,   -- ID del producto
    p_cantidad INT       -- Cantidad del producto
)
AS $$
DECLARE
    v_id_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha);

    SELECT LASTVAL() INTO v_id_pedido;
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
END;
$$ LANGUAGE plpgsql;


-- 🧮 Calcula el total gastado por un cliente Esta función devuelve el 
-- total gastado por un cliente sumando todos sus pedidos.

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC AS $$
DECLARE
    total NUMERIC := 0;  -- Declaramos la variable para el total
BEGIN
    -- Sumar el total de cada pedido del cliente
    SELECT SUM(dp.cantidad * p.precio)
    INTO total
    FROM detalle_pedido dp
    JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
    JOIN productos p ON dp.id_producto = p.id_producto
    WHERE ped.id_cliente = p_id_cliente;

    -- Devolver el total calculado
    RETURN total;
END;
$$ LANGUAGE plpgsql;


-- Crear un trigger que registre en una tabla de auditoría cada vez
-- que se inserte un nuevo pedido, incluyendo el ID del cliente,
-- la fecha del pedido y la fecha y hora del registro.
-- Insertar un nuevo pedido
CREATE OR REPLACE FUNCTION registrar_auditoria_pedido()
RETURNS TRIGGER AS $$
BEGIN
    -- Insertar un registro en la tabla de auditoría
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, CURRENT_TIMESTAMP);

    -- Retornar NEW para continuar con la operación de inserción en la tabla 'pedidos'
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_auditoria_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;


-- Bases de Datos NoSQL (usando JSON en PostgreSQL) Aunque PostgreSQL es una base de datos relacional,
-- permite trabajar con estructuras NoSQL usando
-- tipos de datos como JSON y JSONB.

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

SELECT historial_actividad
FROM usuarios
WHERE nombre = 'Laura Gómez';


-- 🎯 Objetivo Modelar un grafo dirigido donde los nodos son ciudades
-- y las aristas son rutas entre ellas con una distancia.
-- Luego, realizar consultas para explorar las conexiones.

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

SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE r.id_origen = 1;  -- San Luis Potosí

