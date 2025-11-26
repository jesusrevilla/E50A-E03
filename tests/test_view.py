import psycopg2
import unittest

class TestVistaDetallePedidos(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="testdb", user="postgres", password="password", host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_vista_detalle_pedidos(self):
        self.cur.execute("SELECT * FROM vista_detalle_pedidos;")
        result = self.cur.fetchall()
        expected_result = [
            ('Ana Torres', 'Laptop', 1, 1200.00),
            ('Ana Torres', 'Mouse', 2, 51.00),
            ('Luis Pérez', 'Teclado', 1, 45.00)
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

