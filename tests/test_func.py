import psycopg2
import unittest

class TestTotalGastadoPorCliente(unittest.TestCase):

    def setUp(self):
        
        self.conn = psycopg2.connect(
            dbname="testdb", user="postgres", password="password", host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_total_gastado_por_cliente(self):
        
        self.cur.execute("SELECT total_gastado_por_cliente(1);")
        result = self.cur.fetchone()[0]
        self.assertEqual(result, 2401.0)  # Valor esperado basado en datos de ejemplo

if __name__ == '__main__':
    unittest.main()

