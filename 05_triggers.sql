CREATE OR REPLACE FUNCTION fn_auditar_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos(id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auditoria_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_auditar_pedido();
