
BEGIN;

-- Limpiar datos para que IDs sean deterministas
TRUNCATE TABLE
  rutas,
  ciudades,
  auditoria_pedidos,
  detalle_pedido,
  pedidos,
  productos,
  clientes,
  productos_json,
  usuarios
RESTART IDENTITY CASCADE;

-- Evitar ensuciar auditoría con la carga inicial
ALTER TABLE pedidos DISABLE TRIGGER trg_auditar_pedido;

-- -----------------------------
-- Seed relacional (README)
-- -----------------------------
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

ALTER TABLE pedidos ENABLE TRIGGER trg_auditar_pedido;

-- Dejar auditoría limpia para pruebas del trigger
TRUNCATE TABLE auditoria_pedidos RESTART IDENTITY;

-- -----------------------------
-- Seed JSONB (README)
-- -----------------------------
INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop',     '{"marca":"Dell","ram":"16GB","procesador":"Intel i7"}'::jsonb),
('Smartphone', '{"marca":"Samsung","pantalla":"6.5 pulgadas","almacenamiento":"128GB"}'::jsonb),
('Tablet',     '{"marca":"Apple","modelo":"iPad Air","color":"gris"}'::jsonb);

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez', 'laura@example.com',
 '[
   {"fecha":"2025-05-01","accion":"inicio_sesion"},
   {"fecha":"2025-05-02","accion":"subio_archivo"},
   {"fecha":"2025-05-03","accion":"cerro_sesion"}
 ]'::jsonb),
('Pedro Ruiz', 'pedro@example.com',
 '[
   {"fecha":"2025-05-01","accion":"inicio_sesion"},
   {"fecha":"2025-05-04","accion":"comento_publicacion"}
 ]'::jsonb);

-- -----------------------------
-- Seed Grafo (README)
-- -----------------------------
INSERT INTO ciudades (nombre) VALUES
('San Luis Potosí'),
('Querétaro'),
('Guadalajara'),
('Monterrey'),
('CDMX');

INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
(1, 2, 180),
(2, 3, 350),
(1, 5, 410),
(5, 4, 900),
(3, 4, 700);

COMMIT;
