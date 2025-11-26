-- Ciudades (nodos)
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

-- Rutas (aristas)
CREATE TABLE rutas (
    id_origen INT REFERENCES ciudades(id),
    id_destino INT REFERENCES ciudades(id),
    distancia_km INT,
    PRIMARY KEY (id_origen, id_destino)
);

-- Datos de ejemplo
INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'), ('Querétaro'), ('Guadalajara'), ('Monterrey'), ('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1,2,180), (2,3,350), (1,5,410), (5,4,900), (3,4,700);

-- Ver todas las rutas desde San Luis Potosí
SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';
