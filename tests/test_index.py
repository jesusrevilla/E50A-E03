import psycopg2
import pytest

def test_index_existencia_y_definicion():
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

        cur.execute("CREATE INDEX idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);")

        cur.execute("""
            SELECT indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename = 'detalle_pedido' 
              AND indexname = 'idx_cliente_producto';
        """)
        resultado = cur.fetchone()
        
        assert resultado is not None, "El índice 'idx_cliente_producto' no se encontró en la base de datos."
        
        nombre_indice = resultado[0]
        definicion_indice = resultado[1]
        
        assert nombre_indice == 'idx_cliente_producto'
        
        assert 'id_pedido' in definicion_indice, "El índice no incluye la columna id_pedido."
        assert 'id_producto' in definicion_indice, "El índice no incluye la columna id_producto."
        
        assert 'btree' in definicion_indice

    finally:
        if conn:
            cur.close()
            conn.close()
