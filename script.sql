
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


/*---------------------------------------------1--------------------------------------------------------------*/
CREATE VIEW vista_detalle_pedidos AS
SELECT 
    clientes.nombre AS nombre_cliente,
    productos.nombre AS nombre_producto,
    detalle_pedido.cantidad,
    (productos.precio * detalle_pedido.cantidad) AS total_por_linea
FROM detalle_pedido
JOIN pedidos ON detalle_pedido.id_pedido = pedidos.id_pedido
JOIN clientes ON pedidos.id_cliente = clientes.id_cliente
JOIN productos ON detalle_pedido.id_producto = productos.id_producto;

SELECT * FROM vista_detalle_pedidos;

/*---------------------------------------------2--------------------------------------------------------------*/
CREATE PROCEDURE registrar_pedido(
    cliente_id INTEGER,
    fecha_pedido DATE,
    producto_id INTEGER,
    cantidad_producto INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_id_pedido INTEGER;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (cliente_id, fecha_pedido)
    RETURNING id_pedido INTO nuevo_id_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (nuevo_id_pedido, producto_id, cantidad_producto);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

SELECT * FROM pedidos;

/*---------------------------------------------3--------------------------------------------------------------*/

CREATE FUNCTION total_gastado_por_cliente(cliente_id INTEGER)
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
AS $$
    SELECT SUM(productos.precio * detalle_pedido.cantidad)
    FROM pedidos
    JOIN detalle_pedido ON pedidos.id_pedido = detalle_pedido.id_pedido
    JOIN productos ON detalle_pedido.id_producto = productos.id_producto
    WHERE pedidos.id_cliente = cliente_id;
$$;

SELECT total_gastado_por_cliente(1);

CREATE INDEX idx_cliente_producto
ON detalle_pedido (id_pedido, id_producto);

/*---------------------------------------------4--------------------------------------------------------------*/

CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INTEGER,
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

INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');
SELECT * FROM auditoria_pedidos;


/*---------------------------------------------5--------------------------------------------------------------*/

CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}'),
('Telefono', '{"marca": "Samsung", "pantalla": "6.5 pulgadas", "almacenamiento": "128GB"}'),
('Tablet', '{"marca": "Apple", "modelo": "iPad", "color": "gris"}');

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Alfredo De Alba', '177847@upslp.edu.mx', '[
    {"fecha": "2025-05-01", "accion": "inicio_sesion"},
    {"fecha": "2025-05-02", "accion": "subio_archivo"},
    {"fecha": "2025-05-03", "accion": "cerró_sesion"}
]'),
('Alejandro Araujo', '177888@upslp.edu.mx', '[
    {"fecha": "2025-05-01", "accion": "inicio_sesion"},
    {"fecha": "2025-05-04", "accion": "comentó_publicación"},
    {"fecha": "2025-05-03", "accion": "cerró_sesion"}
]');

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT jsonb_array_elements(historial_actividad)->>'accion' AS accion
FROM usuarios
WHERE nombre = 'Alfredo De Alba';


/*---------------------------------------------6-------------------------------------------------------------*/

CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE rutas (
    id_origen INTEGER REFERENCES ciudades(id),
    id_destino INTEGER REFERENCES ciudades(id),
    distancia_km INTEGER,
    PRIMARY KEY (id_origen, id_destino)
);

INSERT INTO ciudades (nombre) VALUES
('San Luis Potosi'), ('Queretaro'), ('Guadalahara'), ('Monterrey'), ('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),
(2, 3, 350),
(1, 5, 410),
(5, 4, 900),
(3, 4, 700);

SELECT 
    ciudad_origen.nombre AS ciudad_origen,
    ciudad_destino.nombre AS ciudad_destino,
    rutas.distancia_km
FROM rutas
JOIN ciudades AS ciudad_origen ON rutas.id_origen = ciudad_origen.id
JOIN ciudades AS ciudad_destino ON rutas.id_destino = ciudad_destino.id
WHERE ciudad_origen.nombre = 'San Luis Potosi';

