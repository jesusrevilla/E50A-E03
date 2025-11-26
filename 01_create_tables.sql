-- Tablas principales
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100)
);



CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha DATE
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES pedidos(id_pedido),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT
);

-- Tabla de auditoría (para Triggers)
CREATE TABLE IF NOT EXISTS auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tablas NoSQL (JSONB)
CREATE TABLE IF NOT EXISTS productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

-- Tablas de Grafos
CREATE TABLE IF NOT EXISTS ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);
