
-- INSERCIÓN DE DATOS EN LA TABLA Cliente
INSERT INTO Cliente (id_cliente, nombre, apellido, email, telefono, direccion) VALUES
(1, 'Ana', 'García', 'ana.garcia@mail.com', '5512345678', 'Av. Reforma 101, CDMX'),
(2, 'Luis', 'Martínez', 'luis.mtz@mail.com', '5587654321', 'Calle Sol 25, Guadalajara'),
(3, 'Sofía', 'Rodríguez', 'sofia.rodriguez@mail.com', '3344556677', 'Paseo de la Luna 8, Monterrey');

-- INSERCIÓN DE DATOS EN LA TABLA Destino
INSERT INTO Destino (id_destino, nombre_ciudad, nombre_pais, descripcion) VALUES
(101, 'París', 'Francia', 'La Ciudad de la Luz, famosa por la Torre Eiffel y el arte.'),
(102, 'Tokio', 'Japón', 'Metrópolis vibrante con templos ancestrales y tecnología de punta.'),
(103, 'Cancún', 'México', 'Playas de arena blanca y aguas turquesas del Caribe.');

-- INSERCIÓN DE DATOS EN LA TABLA Paquete_Turistico
INSERT INTO Paquete_Turistico (id_paquete, nombre_paquete, descripcion, duracion_dias, precio, id_destino) VALUES
(201, 'Escapada Romántica', 'Tour por los museos y cena en la Torre Eiffel.', 5, 1200.50, 101),
(202, 'Aventura Tecnológica', 'Recorrido por Akihabara, Shibuya y el Monte Fuji.', 7, 2500.00, 102),
(203, 'Relax Caribeño', 'Todo incluido en resort frente al mar.', 4, 850.75, 103);

-- INSERCIÓN DE DATOS EN LA TABLA Empleado
INSERT INTO Empleado (id_empleado, nombre, apellido, puesto, fecha_contratacion, salario) VALUES
(301, 'Javier', 'Pérez', 'Agente de Ventas', '2022-03-15', 18000.00),
(302, 'Elena', 'Sánchez', 'Gerente de Reservas', '2021-08-20', 25000.00);

-- INSERCIÓN DE DATOS EN LA TABLA Reserva
INSERT INTO Reserva (id_reserva, id_cliente, id_paquete, id_empleado, fecha_reserva, estado_reserva, monto_total) VALUES
(401, 1, 201, 301, '2023-11-20', 'Confirmada', 1200.50),
(402, 2, 202, 302, '2023-11-22', 'Pendiente', 2500.00),
(403, 3, 203, 301, '2023-11-24', 'Confirmada', 850.75);

-- INSERCIÓN DE DATOS EN LA TABLA Transporte
INSERT INTO Transporte (id_transporte, tipo, nombre_proveedor, costo) VALUES
(501, 'Vuelo', 'AeroViajes', 400.00),
(502, 'Tren', 'RailEurope', 150.00),
(503, 'Bus', 'ADO', 50.00);

-- INSERCIÓN DE DATOS EN LA TABLA Paquete_Transporte
INSERT INTO Paquete_Transporte (id_paquete, id_transporte) VALUES
(201, 501), -- Escapada Romántica usa Vuelo
(201, 502), -- Escapada Romántica usa Tren
(202, 501), -- Aventura Tecnológica usa Vuelo
(203, 501); -- Relax Caribeño usa Vuelo
