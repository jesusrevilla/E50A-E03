CREATE OR REPLACE FUNCTION trg_registrar_auditoria()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);

    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION trg_registrar_auditoria();
