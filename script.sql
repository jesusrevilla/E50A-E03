CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    pr.nombre AS nombre_producto,
    dp.cantidad,
    (dp.cantidad * pr.precio) AS total_por_linea
FROM detalle_pedido dp
JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
JOIN clientes c ON pe.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;


SELECT * FROM vista_detalle_pedidos;

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
    -- 1. Insertamos el pedido y capturamos el ID generado
    INSERT INTO pedidos (id_cliente, fecha) 
    VALUES (p_id_cliente, p_fecha) 
    RETURNING id_pedido INTO v_id_pedido;

    -- 2. Insertamos el detalle asociado a ese pedido
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) 
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
    
    -- Confirmación (opcional en logs)
    RAISE NOTICE 'Pedido % registrado correctamente para el cliente %', v_id_pedido, p_id_cliente;
END;
$$;

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT COALESCE(SUM(pr.precio * dp.cantidad), 0)
    INTO v_total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;

CREATE INDEX idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);

CREATE TABLE auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Crear la función del trigger
CREATE OR REPLACE FUNCTION func_auditoria_pedidos()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insertamos en la tabla de auditoría los datos del NUEVO pedido
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, NOW());
    
    RETURN NEW;
END;
$$;

-- 3. Crear el trigger
CREATE TRIGGER trigger_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION func_auditoria_pedidos();

CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}'),
('Smartphone', '{"marca": "Samsung", "pantalla": "6.5 pulgadas", "almacenamiento": "128GB"}'),
('Tablet', '{"marca": "Apple", "modelo": "iPad Air", "color": "gris"}');

-- Consulta atributo específico (Marca Dell)
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';


-- B) USUARIOS E HISTORIAL -----------------------
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

-- Consultar usuarios que realizaron "inicio_sesion"
-- Usamos el operador de contención @>
SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

-- Extraer todas las acciones de un usuario (Desglosar el JSON Array)
-- Esto convierte el array JSON en filas individuales
SELECT 
    nombre, 
    elemento ->> 'fecha' as fecha,
    elemento ->> 'accion' as accion
FROM usuarios,
LATERAL jsonb_array_elements(historial_actividad) as elemento
WHERE nombre = 'Laura Gómez';


-- ==========================================================
-- 6. GRAFOS
-- ==========================================================

-- 1. Crear tablas
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

-- 2. Insertar datos
INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),  -- SLP -> Querétaro
(2, 3, 350),  -- Querétaro -> Guadalajara
(1, 5, 410),  -- SLP -> CDMX
(5, 4, 900),  -- CDMX -> Monterrey
(3, 4, 700);  -- Guadalajara -> Monterrey

-- 3. Consulta: Ver todas las rutas directas desde San Luis Potosí
-- Hacemos JOIN para obtener los nombres en lugar de solo IDs
SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';
