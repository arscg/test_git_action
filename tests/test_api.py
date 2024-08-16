import unittest
from app import app, db
from werkzeug.security import generate_password_hash

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

        # Création d'un utilisateur de test
        hashed_password = generate_password_hash('password', method='sha256')
        user = User(username='testuser', password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Authentification et récupération du token
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'password'})
        self.token = response.get_json()['token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_data_animov_ch(self):
        # Tester la route get_data_animov_ch avec les paramètres requis
        response = self.app.get('/get_data_animov_ch', headers={'x-access-tokens': self.token}, query_string={
            'sources': '1,2',  # Exemple de sources valides
            'with_images': 'False',
            'with_detect': 'False',
            'with_stats': 'True',
            'with_global_stats': 'True'
        })

        # Vérifier que la requête est réussie
        self.assertEqual(response.status_code, 200)

        # Vérifier que la réponse contient les champs attendus
        json_data = response.get_json()
        self.assertIn('_general_stats', json_data)
        self.assertIn('_send_date', json_data)

if __name__ == '__main__':
    unittest.main()
