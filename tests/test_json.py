import psycopg2

def test_json_marca_dell():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("""
        SELECT * 
        FROM productos_json 
        WHERE atributos ->> 'marca' = 'Dell';
    """)
    
    resultado = cur.fetchall()
    assert len(resultado) == 1

