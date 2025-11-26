-- Función para obtener el salario promedio por departamento
CREATE OR REPLACE FUNCTION get_salario_promedio_departamento(depto VARCHAR)
RETURNS NUMERIC AS $$
DECLARE
    salario_promedio NUMERIC;
BEGIN
    SELECT AVG(salario) INTO salario_promedio
    FROM empleados
    WHERE departamento = depto;

    RETURN salario_promedio;
END;
$$ LANGUAGE plpgsql;

-- Trigger para auditar cambios de salario
CREATE OR REPLACE FUNCTION auditar_cambio_salario()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.salario IS DISTINCT FROM NEW.salario THEN
        INSERT INTO auditoria_salarios (empleado_id, salario_antiguo, salario_nuevo)
        VALUES (NEW.id, OLD.salario, NEW.salario);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_auditar_salario
AFTER UPDATE OF salario ON empleados
FOR EACH ROW
EXECUTE FUNCTION auditar_cambio_salario();
