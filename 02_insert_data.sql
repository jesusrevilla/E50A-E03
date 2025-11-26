-- Datos de Productos 
INSERT INTO productos (nombre, etiquetas) VALUES
('Laptop Gamer', ARRAY['tecnología', 'computadora', 'gaming']),
('Teclado Mecánico', ARRAY['tecnología', 'periférico']),
('Silla de Oficina', ARRAY['mueble', 'oficina']),
('Monitor 4K', ARRAY['tecnología', 'pantalla', 'oficina']);

-- Datos de Ciudades y Rutas (Grafo)
INSERT INTO ciudades (nombre) VALUES 
('Ciudad A'), ('Ciudad B'), ('Ciudad C'), ('Ciudad D');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 100), -- A a B
(2, 3, 200); -- B a C
