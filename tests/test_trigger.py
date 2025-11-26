import pytest
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_trigger_auditoria_insert():
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-12-31') RETURNING id_pedido;")
        id_pedido_nuevo = cur.fetchone()[0]
        conn.commit()
        
        cur.execute("""
            SELECT id_auditoria, fecha_registro 
            FROM auditoria_pedidos 
            WHERE id_cliente = 2 AND fecha_pedido = '2025-12-31'
            ORDER BY id_auditoria DESC LIMIT 1;
        """)
        auditoria = cur.fetchone()
        
        assert auditoria is not None, "El trigger no insertó el registro en auditoria_pedidos"
        
    finally:
        cur.close()
        conn.close()
