from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import CustomUser


class AuthBasicTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        """Тест успешной регистрации (без ролей и правил)"""
        data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'password_repeat': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CustomUser.objects.filter(email='test@example.com').exists(),
        )

    def test_register_password_mismatch(self):
        """Пароли не совпадают HTTP_400_BAD_REQUEST"""
        data = {
            'email': 'test2@example.com',
            'password': 'pass1',
            'password_repeat': 'pass2',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_credentials(self):
        """Неверный пароль HTTP_401_UNAUTHORIZED"""
        user = CustomUser.objects.create(
            email='wrong@test.com',
            first_name='Wrong',
            last_name='User',
        )
        user.set_password('correctpass')
        user.save()
        response = self.client.post(
            '/api/auth/login/',
            {'email': 'wrong@test.com', 'password': 'wrongpass'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_account(self):
        """Удаление аккаунта (мягкое) TTP_200_OK + is_active=False"""
        user = CustomUser.objects.create(
            email='delete@test.com',
            first_name='Delete',
            last_name='Me',
        )
        user.set_password('deletepass')
        user.save()
        login_resp = self.client.post(
            '/api/auth/login/',
            {'email': 'delete@test.com', 'password': 'deletepass'},
            format='json',
        )
        token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete('/api/auth/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            email='old@test.com',
            first_name='Old',
            last_name='User',
        )
        user.set_password('pass123')
        user.save()
        login_resp = self.client.post(
            '/api/auth/login/',
            {'email': 'old@test.com', 'password': 'pass123'},
            format='json',
        )
        token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(
            '/api/auth/profile/',
            {'first_name': 'New', 'email': 'new@test.com'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'New')
        self.assertEqual(response.data['email'], 'new@test.com')
