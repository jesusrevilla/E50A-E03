import psycopg2
import unittest

class TestProductosJson(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="testdb", user="postgres", password="password", host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_consultar_producto_por_marca(self):
        self.cur.execute("""
            SELECT * FROM productos_json
            WHERE atributos ->> 'marca' = 'Dell';
        """)
        result = self.cur.fetchall()
        self.assertEqual(len(result), 1)  # Debe haber solo un producto con la marca 'Dell'

if __name__ == '__main__':
    unittest.main()

