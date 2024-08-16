import unittest
import test_data_animov
# from test_data_animov import app
# from app import db
# from werkzeug.security import generate_password_hash
# from models import User

class ApiTestCase(unittest.TestCase):
    # def setUp(self):
    #     self.app = app.test_client()
    #     with app.app_context():
    #         db.create_all()  # Crée toutes les tables

    #     # Supprimer l'utilisateur si nécessaire
    #     user = User.query.filter_by(username='testuser').first()
    #     if user:
    #         db.session.delete(user)
    #         db.session.commit()

    #     # Ajouter un utilisateur de test
    #     hashed_password = generate_password_hash('password', method='sha256')
    #     user = User(username='testuser', password=hashed_password)
    #     db.session.add(user)
    #     db.session.commit()

    #     # Authentification et récupération du token
    #     response = self.app.post('/login', json={'username': 'testuser', 'password': 'password'})
    #     self.token = response.get_json().get('token', None)

    # def tearDown(self):
    #     with app.app_context():
    #         db.session.remove()
    #         db.drop_all()  # Supprime toutes les tables après les tests

    def test_get_data_animov_ch(self):
        response = self.app.get('/get_data_animov_ch', headers={'x-access-tokens': self.token}, query_string={
            'sources': '1,2',
            'with_images': 'False',
            'with_detect': 'False',
            'with_stats': 'True',
            'with_global_stats': 'True'
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
