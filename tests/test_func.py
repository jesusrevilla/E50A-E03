def test_total_gastado_ana_torres(cursor):
    # Ana Torres (id=1): 1 Laptop (1200) + 2 Mouse (2 * 25.50 = 51.00) = 1251.00
    cursor.execute("SELECT total_gastado_por_cliente(1)")
    total = cursor.fetchone()[0]
    assert total == 1251.00

def test_total_gastado_luis_perez(cursor):
    # Luis Pérez (id=2): 1 Teclado (45.00) = 45.00
    cursor.execute("SELECT total_gastado_por_cliente(2)")
    total = cursor.fetchone()[0]
    assert total == 45.00
