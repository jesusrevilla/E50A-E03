
-- TABLA 1: Cliente
CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    direccion VARCHAR(255)
);

-- TABLA 2: Destino
CREATE TABLE Destino (
    id_destino INT PRIMARY KEY,
    nombre_ciudad VARCHAR(100),
    nombre_pais VARCHAR(100),
    descripcion TEXT
);

-- TABLA 3: Paquete_Turistico
CREATE TABLE Paquete_Turistico (
    id_paquete INT PRIMARY KEY,
    nombre_paquete VARCHAR(100),
    descripcion TEXT,
    duracion_dias INT,
    precio DECIMAL(10, 2),
    id_destino INT,
    FOREIGN KEY (id_destino) REFERENCES Destino(id_destino)
);

-- TABLA 4: Empleado
CREATE TABLE Empleado (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    puesto VARCHAR(50),
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
);

-- TABLA 5: Reserva
-- Esta tabla enlaza Clientes, Paquetes y Empleados (quien realiza la reserva)
CREATE TABLE Reserva (
    id_reserva INT PRIMARY KEY,
    id_cliente INT,
    id_paquete INT,
    id_empleado INT,
    fecha_reserva DATE,
    estado_reserva VARCHAR(50), -- Ej: Confirmada, Pendiente, Cancelada
    monto_total DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_paquete) REFERENCES Paquete_Turistico(id_paquete),
    FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado)
);

-- TABLA 6: Transporte (Opcional, pero útil para paquetes)
CREATE TABLE Transporte (
    id_transporte INT PRIMARY KEY,
    tipo VARCHAR(50), -- Ej: Vuelo, Tren, Bus
    nombre_proveedor VARCHAR(100),
    costo DECIMAL(10, 2)
);

-- TABLA 7: Paquete_Transporte (Tabla intermedia para relación N:M)
CREATE TABLE Paquete_Transporte (
    id_paquete INT,
    id_transporte INT,
    PRIMARY KEY (id_paquete, id_transporte),
    FOREIGN KEY (id_paquete) REFERENCES Paquete_Turistico(id_paquete),
    FOREIGN KEY (id_transporte) REFERENCES Transporte(id_transporte)
);
