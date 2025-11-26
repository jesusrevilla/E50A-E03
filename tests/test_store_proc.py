import psycopg2
import pytest
import os

def test_registrar_pedido():
    # Conexión a la base de datos usando las variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()

    # Ejecutar el procedimiento almacenado
    cur.execute("""
        CALL registrar_pedido(1, '2025-05-20', 2, 3);
    """)

    # Verificar si el pedido se ha insertado
    cur.execute("SELECT * FROM pedidos WHERE id_cliente = 1 AND fecha = '2025-05-20';")
    result = cur.fetchone()

    assert result is not None

    cur.close()
    conn.close()
