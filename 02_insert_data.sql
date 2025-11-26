INSERT INTO clientes (nombre, correo) VALUES
('Ana Torres', 'ana@example.com'),
('Luis Pérez', 'luis@example.com');

INSERT INTO productos (nombre, precio) VALUES
('Laptop', 1200.00),
('Mouse', 25.50),
('Teclado', 45.00);

INSERT INTO pedidos (id_cliente, fecha) VALUES
(1, '2025-05-01'),
(2, '2025-05-02');

INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES
(1, 1, 1),  
(1, 2, 2),  
(2, 3, 1);  

INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),  
(2, 3, 350),  
(1, 5, 410),  
(5, 4, 900),  
(3, 4, 700);  
