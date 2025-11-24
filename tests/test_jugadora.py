import unittest, os
from app import create_app, db
from app.models import Jugadora

class TestJugadora(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_jugadora_creation(self):
        print('Ejecutando test_jugadora_creation')
        response = self.client.post('/jugadoras', json={
            'nombre': 'Test Jugadora',
            'apellido': 'Delantera'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Jugadora', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
