INSERT INTO clientes (nombre, correo) VALUES
('Ana Torres', 'ana@example.com'),
('Luis Pérez', 'luis@example.com');

-- Inserción de datos en la tabla productos
INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200.00),
('Mouse', 25.50),
('Teclado', 45.00);

-- Inserción de datos en la tabla pedidos
INSERT INTO pedidos (id_cliente, fecha) VALUES
(1, '2025-05-01'),
(2, '2025-05-02');

-- Inserción de datos en la tabla detalle_pedido
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES
(1, 1, 1),  -- Ana compra 1 Laptop
(1, 2, 2),  -- Ana compra 2 Mouse
(2, 3, 1);  -- Luis compra 1 Teclado

-- Inserción de datos para el ejercicio de Grafos (Ciudades)
INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

-- Inserción de datos para el ejercicio de Grafos (Rutas)
INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),  -- SLP → Querétaro
(2, 3, 350),  -- Querétaro → Guadalajara
(1, 5, 410),  -- SLP → CDMX
(5, 4, 900),  -- CDMX → Monterrey
(3, 4, 700);  -- Guadalajara → Monterrey
