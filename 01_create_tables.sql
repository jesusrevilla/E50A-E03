CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    salario NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS auditoria_salarios (
    id SERIAL PRIMARY KEY,
    empleado_id INTEGER REFERENCES empleados(id),
    salario_antiguo NUMERIC(10, 2),
    salario_nuevo NUMERIC(10, 2),
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
