
DROP VIEW IF EXISTS vista_detalle_pedidos;

-- Luego eliminar tablas en orden seguro
DROP TABLE IF EXISTS auditoria_pedidos;
DROP TABLE IF EXISTS detalle_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;

DROP TABLE IF EXISTS productos_json;
DROP TABLE IF EXISTS usuarios;

DROP TABLE IF EXISTS rutas;
DROP TABLE IF EXISTS ciudades;

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre     VARCHAR(100),
    correo     VARCHAR(100)
);

CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre      VARCHAR(100),
    precio      DECIMAL(10, 2)
);

CREATE TABLE pedidos (
    id_pedido  SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    fecha      DATE
);

CREATE TABLE detalle_pedido (
    id_detalle  SERIAL PRIMARY KEY,
    id_pedido   INT REFERENCES pedidos(id_pedido),
    id_producto INT REFERENCES productos(id_producto),
    cantidad    INT
);


CREATE TABLE auditoria_pedidos (
    id_auditoria   SERIAL PRIMARY KEY,
    id_cliente     INT,
    fecha_pedido   DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE productos_json (
    id        SERIAL PRIMARY KEY,
    nombre    TEXT,
    atributos JSONB
);


CREATE TABLE usuarios (
    id                  SERIAL PRIMARY KEY,
    nombre              TEXT,
    correo              TEXT,
    historial_actividad JSONB
);


CREATE TABLE ciudades (
    id     SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE rutas (
    id_origen    INT REFERENCES ciudades(id),
    id_destino   INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);