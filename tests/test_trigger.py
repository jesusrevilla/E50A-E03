import psycopg2
import pytest
from datetime import date

def test_trigger_auditoria_pedidos():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname='test_db',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS auditoria_pedidos, detalle_pedido, pedidos, clientes CASCADE;")
        
        cur.execute("""
            CREATE TABLE clientes (id_cliente SERIAL PRIMARY KEY, nombre VARCHAR(100), correo VARCHAR(100));
            
            CREATE TABLE pedidos (
                id_pedido SERIAL PRIMARY KEY, 
                id_cliente INT REFERENCES clientes(id_cliente), 
                fecha DATE
            );
            
            CREATE TABLE auditoria_pedidos (
                id_auditoria SERIAL PRIMARY KEY, 
                id_cliente INT, 
                fecha_pedido DATE, 
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE OR REPLACE FUNCTION fn_registrar_auditoria_pedido()
            RETURNS TRIGGER AS $$
            BEGIN
                INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
                VALUES (NEW.id_cliente, NEW.fecha, NOW());
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

        cur.execute("""
            CREATE TRIGGER trg_auditoria_nuevo_pedido
            AFTER INSERT ON pedidos
            FOR EACH ROW
            EXECUTE FUNCTION fn_registrar_auditoria_pedido();
        """)

        cur.execute("INSERT INTO clientes (nombre, correo) VALUES ('Cliente Test', 'test@mail.com');")

        cur.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
        assert cur.fetchone()[0] == 0, "La tabla de auditoría debería estar vacía al inicio."

        fecha_prueba = date(2025, 12, 25)
        
        cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, %s);", (fecha_prueba,))
        cur.execute("SELECT * FROM auditoria_pedidos;")
        auditoria = cur.fetchone()
        
        assert auditoria is not None, "El trigger NO se disparó (la tabla auditoria sigue vacía)."
        
        id_cliente_auditado = auditoria[1]
        fecha_auditada = auditoria[2]
        
        assert id_cliente_auditado == 1, f"El ID de cliente en auditoría es incorrecto. Esperado 1, obtenido {id_cliente_auditado}"
        assert fecha_auditada == fecha_prueba, f"La fecha en auditoría es incorrecta. Esperado {fecha_prueba}, obtenido {fecha_auditada}"

    finally:
        if conn:
            cur.close()
            conn.close()
