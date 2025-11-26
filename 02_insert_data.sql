-- 1. Datos de Productos (Arrays)
INSERT INTO productos (nombre, etiquetas) VALUES
('Laptop Gamer', ARRAY['tecnología', 'computadora', 'gaming']),
('Teclado Mecánico', ARRAY['tecnología', 'periférico']),
('Silla de Oficina', ARRAY['mueble', 'oficina']),
('Monitor 4K', ARRAY['tecnología', 'pantalla', 'oficina']);

-- 2. Datos de Ciudades y Rutas (Grafo)
INSERT INTO ciudades (id, nombre) VALUES 
(1, 'Ciudad A'), 
(2, 'Ciudad B'), 
(3, 'Ciudad C'), 
(4, 'Ciudad D');

-- Rutas: A -> B -> C
INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 100), -- A a B
(2, 3, 200); -- B a C
