import psycopg2
import unittest

class TestTriggerAuditoria(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="testdb", user="postgres", password="password", host="localhost", port="5432"
        )
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_trigger_auditoria(self):
        # Insertar un nuevo pedido para probar el trigger
        self.cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');")
        self.conn.commit()

        # Verificar si el trigger ha insertado en la tabla de auditoría
        self.cur.execute("SELECT * FROM auditoria_pedidos WHERE id_cliente = 1;")
        result = self.cur.fetchall()
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()

