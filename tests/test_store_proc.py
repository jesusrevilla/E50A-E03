import psycopg2
import pytest
from datetime import date

def test_procedure_registrar_pedido():
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
        cur.execute("DROP TABLE IF EXISTS detalle_pedido, pedidos, productos, clientes CASCADE;")
        
        cur.execute("""
            CREATE TABLE clientes (id_cliente SERIAL PRIMARY KEY, nombre VARCHAR(100), correo VARCHAR(100));
            CREATE TABLE productos (id_producto SERIAL PRIMARY KEY, nombre VARCHAR(100), precio DECIMAL(10, 2));
            CREATE TABLE pedidos (id_pedido SERIAL PRIMARY KEY, id_cliente INT REFERENCES clientes(id_cliente), fecha DATE);
            CREATE TABLE detalle_pedido (id_detalle SERIAL PRIMARY KEY, id_pedido INT REFERENCES pedidos(id_pedido), id_producto INT REFERENCES productos(id_producto), cantidad INT);
        """)

        cur.execute("INSERT INTO clientes (nombre, correo) VALUES ('Cliente Proc', 'proc@test.com');") 
        cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Producto Proc', 100.00);")       

        cur.execute("""
            CREATE OR REPLACE PROCEDURE registrar_pedido(
                p_id_cliente INT,
                p_fecha DATE,
                p_id_producto INT,
                p_cantidad INT
            )
            LANGUAGE plpgsql
            AS $$
            DECLARE
                v_id_pedido_generado INT;
            BEGIN
                -- 1. Insertar Cabecera
                INSERT INTO pedidos (id_cliente, fecha)
                VALUES (p_id_cliente, p_fecha)
                RETURNING id_pedido INTO v_id_pedido_generado;

                -- 2. Insertar Detalle vinculado
                INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
                VALUES (v_id_pedido_generado, p_id_producto, p_cantidad);
            END;
            $$;
        """)

        cliente_id = 1
        producto_id = 1
        cantidad_compra = 5
        fecha_compra = date(2025, 10, 20)

        cur.execute("CALL registrar_pedido(%s, %s, %s, %s);", 
                    (cliente_id, fecha_compra, producto_id, cantidad_compra))
        cur.execute("SELECT id_pedido, id_cliente, fecha FROM pedidos WHERE id_cliente = %s;", (cliente_id,))
        pedido = cur.fetchone()

        assert pedido is not None, "El procedimiento no creó el registro en la tabla 'pedidos'."
        
        id_pedido_creado = pedido[0]
        assert pedido[1] == cliente_id
        assert pedido[2] == fecha_compra
        cur.execute("SELECT id_producto, cantidad FROM detalle_pedido WHERE id_pedido = %s;", (id_pedido_creado,))
        detalle = cur.fetchone()

        assert detalle is not None, "El procedimiento no creó el registro en 'detalle_pedido'."
        assert detalle[0] == producto_id, "El ID del producto en el detalle es incorrecto."
        assert detalle[1] == cantidad_compra, "La cantidad en el detalle es incorrecta."

    finally:
        if conn:
            cur.close()
            conn.close()
