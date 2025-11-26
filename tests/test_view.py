import psycopg2
import pytest
from decimal import Decimal

def test_vista_detalle_pedidos():
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

        cur.execute("DROP VIEW IF EXISTS vista_detalle_pedidos;")
        cur.execute("DROP TABLE IF EXISTS detalle_pedido, pedidos, productos, clientes CASCADE;")
        
        cur.execute("""
            CREATE TABLE clientes (id_cliente SERIAL PRIMARY KEY, nombre VARCHAR(100), correo VARCHAR(100));
            CREATE TABLE productos (id_producto SERIAL PRIMARY KEY, nombre VARCHAR(100), precio DECIMAL(10, 2));
            CREATE TABLE pedidos (id_pedido SERIAL PRIMARY KEY, id_cliente INT REFERENCES clientes(id_cliente), fecha DATE);
            CREATE TABLE detalle_pedido (id_detalle SERIAL PRIMARY KEY, id_pedido INT REFERENCES pedidos(id_pedido), id_producto INT REFERENCES productos(id_producto), cantidad INT);
        """)

        cur.execute("INSERT INTO clientes (nombre, correo) VALUES ('Juan Test', 'juan@test.com');")
      
        cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Monitor', 200.50);")

        cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-06-01');")
        
        cur.execute("INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES (1, 1, 3);")

        cur.execute("""
            CREATE VIEW vista_detalle_pedidos AS
            SELECT 
                c.nombre AS nombre_cliente,
                p.nombre AS nombre_producto,
                dp.cantidad,
                (dp.cantidad * p.precio) AS total_linea
            FROM 
                detalle_pedido dp
                JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
                JOIN clientes c ON pe.id_cliente = c.id_cliente
                JOIN productos p ON dp.id_producto = p.id_producto;
        """)

        cur.execute("SELECT * FROM vista_detalle_pedidos WHERE nombre_cliente = 'Juan Test';")
        resultado = cur.fetchone()
        
        assert resultado is not None, "La vista no devolvió registros."
        assert resultado[0] == 'Juan Test', "El nombre del cliente en la vista es incorrecto."
        assert resultado[1] == 'Monitor', "El nombre del producto en la vista es incorrecto."
        
        assert resultado[2] == 3, "La cantidad en la vista es incorrecta."
        
        total_esperado = Decimal('601.50')
        assert resultado[3] == total_esperado, f"Cálculo matemático incorrecto. Esperado {total_esperado}, obtenido {resultado[3]}"

    finally:
        if conn:
            cur.close()
            conn.close()
