import psycopg2
import unittest

class TestIndiceCompuesto(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="testdb", user="postgres", password="password", host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_crear_indice_compuesto(self):
        # Verificar que el índice ha sido creado correctamente
        self.cur.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE indexname = 'idx_cliente_producto';
        """)
        result = self.cur.fetchone()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()

