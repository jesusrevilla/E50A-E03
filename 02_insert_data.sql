-- Insertar clientes
INSERT INTO clientes (nombre, correo) VALUES
('Ana Torres', 'ana@example.com'),
('Luis Pérez', 'luis@example.com'),
('María López', 'maria@example.com');

-- Insertar productos
INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200.00),
('Mouse', 25.50),
('Teclado', 45.00),
('Monitor', 300.00);

-- Insertar pedidos
INSERT INTO pedidos (id_cliente, fecha) VALUES
(1, '2025-05-01'),  -- Ana
(2, '2025-05-02'),  -- Luis
(3, '2025-05-03');  -- María

-- Insertar detalle de pedidos
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES
(1, 1, 1),  -- Ana compra 1 Laptop
(1, 2, 2),  -- Ana compra 2 Mouse
(2, 3, 1),  -- Luis compra 1 Teclado
(3, 4, 2);  -- María compra 2 Monitores

