# import unittest
from test_data_animov import app

# class ApiTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

#     def test_get_data_animov_ch(self):
#         # response = self.app.get('/get_data_animov_ch', headers={'x-access-tokens': self.token}, query_string={
#         response = self.app.get('/get_data_animov_ch', query_string={
#             'sources': '1,2',
#             'with_images': 'False',
#             'with_detect': 'False',
#             'with_stats': 'True',
#             'with_global_stats': 'True'
#         })
#         self.assertEqual(response.status_code, 200)

#     #  def test_dates_route(self):
#     #     # Utiliser un token valide pour les tests
#     #     token = 'votre_token_valide_ici'  # Remplacez par un token valide
#     #     headers = {'x-access-tokens': token}

#     #     response = self.app.get('/dates', headers=headers)
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIsInstance(json.loads(response.data), list)  # Vérifiez que la réponse est une liste
#     #     self.assertTrue(len(json.loads(response.data)) > 0)  # Vérifiez que la liste n'est pas vide

#     def test_dates_route_without_token(self):
#         response = self.app.get('/dates')
#         self.assertEqual(response.status_code, 401)  # Vérifie que l'accès sans token retourne un statut 401
#         self.assertIn(b'Token manquant', response.data)  # Vérifie que le message 'Token manquant' est dans la réponse

# if __name__ == '__main__':
#     unittest.main()

# tests/test_dates_route.py

import pytest
# from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_dates_route_without_token(client):
    response = client.get('/dates')
    assert response.status_code == 401  # Vérifie que l'accès sans token retourne un statut 401
    assert b'Token manquant' in response.data  # Vérifie que le message 'Token manquant' est dans la réponse
