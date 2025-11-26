DROP TABLE IF EXISTS rutas;
DROP TABLE IF EXISTS ciudades;
DROP TABLE IF EXISTS productos;

-- Tabla para ejercicio de Arrays
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    etiquetas TEXT[] -- Array de texto
);

-- Tablas para ejercicio de Grafos
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT
);
