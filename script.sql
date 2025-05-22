

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





/* Crear una vista con JOINs (vista_detalle_pedidos) 
esta vista muestra el detalle de cada pedido, 
incluyendo el nombre del cliente, producto, cantidad y el total por línea.*/

CREATE VIEW vista_detalle_pedidos AS
SELECT 
p.id_pedido,
c.nombre AS Clientes,
pr.nombre AS productos,
dp.cantidad,
dp.cantidad * pr.precio AS total_por_linea
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
JOIN productos pr ON dp.id_producto = pr.id_producto;

/* Registrar un nuevo pedido Este procedimiento llamado registrar_pedido 
inserta un nuevo pedido y sus detalles en varias tablas.*/






/* Calcula el total gastado por un cliente Esta función devuelve
el total gastado por un cliente sumando todos sus pedidos.*/

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(id_clientes INT)
RETURNS NUMERIC AS $$
DECLARE total NUMERIC;
BEGIN
--EN ESTA PARTE UTILICE COALESCE YA QUE PERIMITE TOMAR EL PRIMER REGISTRO NO NULLO DE UNA LISTA
--EN ESTE CASO EL PRIMER CLIENTE 
  SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)
  INTO total
  FROM pedidos p
  JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
  JOIN productos pr ON dp.id_producto = pr.id_producto
  WHERE p.id_cliente = id_clientes;

  RETURN total;
END;
$$ LANGUAGE plpgsql;






/*Disparadores (Triggers)*/
--FUNCION PARA TRIGGER
--TABLA ADICIONAL 

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
BEFORE UPDATE ON auditoria_pedidos
FOR EACH ROW
EXECUTE PROCEDURE registrar_auditoria_pedido();









--PROBLEMA 1
SELECT * FROM vista_detalle_pedidos;

--PROBLEMA 2

--PROBLEMA 3
SELECT total_gastado_por_cliente(1);

--PROBLEMA 4
-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;






