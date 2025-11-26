import psycopg2
import pytest
import os

def test_trigger_auditoria():
    # Conexión a la base de datos usando las variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()

    # Insertar un nuevo pedido
    cur.execute("""
        INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');
    """)

    # Verificar si la auditoría se registró correctamente
    cur.execute("""
        SELECT * FROM auditoria_pedidos WHERE id_cliente = 1 AND fecha_pedido = '2025-05-20';
    """)
    result = cur.fetchone()

    # Comprobar que el registro de auditoría existe
    assert result is not None

    cur.close()
    conn.close()


