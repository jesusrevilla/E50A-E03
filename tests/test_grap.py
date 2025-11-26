import psycopg2
import unittest

class TestGrafoCiudades(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="testdb", user="postgres", password="password", host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_rutas_desde_sanluis(self):
        self.cur.execute("""
            SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
            FROM rutas r
            JOIN ciudades c1 ON r.id_origen = c1.id
            JOIN ciudades c2 ON r.id_destino = c2.id
            WHERE c1.nombre = 'San Luis Potosí';
        """)
        result = self.cur.fetchall()
        expected_result = [('San Luis Potosí', 'Querétaro', 180), ('San Luis Potosí', 'CDMX', 410)]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

