import psycopg2
import pytest
from decimal import Decimal

def test_funcion_total_gastado(db_conn=None):
    conn = None
    try:
        # Configura tu conexión aquí
        conn = psycopg2.connect(
            dbname='test_db',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS auditoria_pedidos, detalle_pedido, pedidos, productos, clientes CASCADE;")
        
        cur.execute("""
            CREATE TABLE clientes (id_cliente SERIAL PRIMARY KEY, nombre VARCHAR(100), correo VARCHAR(100));
            CREATE TABLE productos (id_producto SERIAL PRIMARY KEY, nombre VARCHAR(100), precio DECIMAL(10, 2));
            CREATE TABLE pedidos (id_pedido SERIAL PRIMARY KEY, id_cliente INT REFERENCES clientes(id_cliente), fecha DATE);
            CREATE TABLE detalle_pedido (id_detalle SERIAL PRIMARY KEY, id_pedido INT REFERENCES pedidos(id_pedido), id_producto INT REFERENCES productos(id_producto), cantidad INT);
        """)

        cur.execute("""
            INSERT INTO clientes (nombre, correo) VALUES ('Ana Torres', 'ana@test.com'), ('Luis Pérez', 'luis@test.com');
            INSERT INTO productos (nombre, precio) VALUES ('Laptop', 1200.00), ('Mouse', 25.50), ('Teclado', 45.00);
            
            -- Pedidos iniciales
            INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-01'), (2, '2025-05-02');
            
            -- Detalle: 
            -- Ana (ID 1): 1 Laptop (1200) + 2 Mouse (25.50 * 2 = 51.00) = TOTAL 1251.00
            -- Luis (ID 2): 1 Teclado (45.00) = TOTAL 45.00
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES 
            (1, 1, 1), 
            (1, 2, 2), 
            (2, 3, 1);
        """)

        cur.execute("""
            CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
            RETURNS DECIMAL(10, 2)
            LANGUAGE plpgsql
            AS $$
            DECLARE
                v_total DECIMAL(10, 2);
            BEGIN
                SELECT COALESCE(SUM(dp.cantidad * p.precio), 0)
                INTO v_total
                FROM pedidos pe
                JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
                JOIN productos p ON dp.id_producto = p.id_producto
                WHERE pe.id_cliente = p_id_cliente;
                RETURN v_total;
            END;
            $$;
        """)
        cur.execute("SELECT total_gastado_por_cliente(1);")
        resultado_ana = cur.fetchone()[0]
        assert resultado_ana == Decimal('1251.00'), f"Error en cálculo de Ana. Esperado 1251.00, obtenido {resultado_ana}"

        cur.execute("SELECT total_gastado_por_cliente(2);")
        resultado_luis = cur.fetchone()[0]
        assert resultado_luis == Decimal('45.00'), f"Error en cálculo de Luis. Esperado 45.00, obtenido {resultado_luis}"

        cur.execute("INSERT INTO clientes (nombre, correo) VALUES ('Nuevo', 'nuevo@test.com');")
        cur.execute("SELECT total_gastado_por_cliente(3);")
        resultado_nuevo = cur.fetchone()[0]
        assert resultado_nuevo == Decimal('0.00'), f"Error en cliente vacío. Esperado 0.00, obtenido {resultado_nuevo}"

    finally:
        if conn:
            cur.close()
            conn.close()
