import psycopg2

def test_trigger_auditoria():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-06-01');")
    conn.commit()

    cur.execute("""
        SELECT COUNT(*) 
        FROM auditoria_pedidos 
        WHERE fecha_pedido='2025-06-01';
    """)
    
    registros = cur.fetchone()[0]
    assert registros >= 1

