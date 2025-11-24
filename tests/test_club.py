import unittest, os
from app import create_app, db


class TestClub(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_club_creation(self):
        print('Ejecutando test_club_creation')
        response = self.client.post('/clubs', json={
            'nombre': 'Test Club'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Club', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
