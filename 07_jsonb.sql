-- Productos con atributos flexibles
CREATE TABLE productos_json (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    atributos JSONB
);

INSERT INTO productos_json (nombre, atributos) VALUES
('Laptop', '{"marca":"Dell","ram":"16GB","procesador":"Intel i7"}'),
('Smartphone', '{"marca":"Samsung","pantalla":"6.5 pulgadas","almacenamiento":"128GB"}');

-- Usuarios con historial de actividad
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    correo TEXT,
    historial_actividad JSONB
);

INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
('Laura Gómez','laura@example.com',
 '[{"fecha":"2025-05-01","accion":"inicio_sesion"},
   {"fecha":"2025-05-02","accion":"subio_archivo"}]');
