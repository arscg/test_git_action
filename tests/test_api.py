import unittest
from app import app, db
from models import User, Product
from werkzeug.security import generate_password_hash

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

        hashed_password = generate_password_hash('password', method='sha256')
        user = User(username='testuser', password=hashed_password)
        db.session.add(user)

        product1 = Product(name='Product1', price=10.99)
        product2 = Product(name='Product2', price=15.99)
        db.session.add(product1)
        db.session.add(product2)

        db.session.commit()

        response = self.app.post('/login', json={'username': 'testuser', 'password': 'password'})
        self.token = response.get_json()['token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_products(self):
        response = self.app.get('/products', headers={'x-access-tokens': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_get_data_animov_ch(self):
        params = {
            'sources': '1,2',
            'with_images': 'False',
            'with_detect': 'False',
            'with_stats': 'True',
            'with_global_stats': 'True'
        }
        response = self.app.get('/get_data_animov_ch', headers={'x-access-tokens': self.token}, query_string=params)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('_general_stats', json_data)
        self.assertIn('_send_date', json_data)

if __name__ == '__main__':
    unittest.main()
