from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse

class AuthTests(APITestCase):
    def setUp(self):
        # ユーザーを作成
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_login(self):
        # ログインデータを用意
        url = reverse('api_login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        
        # POSTリクエストでログインをテスト
        response = self.client.post(url, data, format='json')
        
        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # トークンが返されていることを確認
        self.assertIn('token', response.data)
        
        # トークンの一致を確認
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)
