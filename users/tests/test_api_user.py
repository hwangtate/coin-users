from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserRegisterTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("user_register")
        self.data = {
            "nickname": "test user",
            "email": "test@example.com",
            "password": "Qwea1287!",
            "password2": "Qwea1287!",
        }

    def test_user_registration(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.first().nickname, "test user")


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("user_login")
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="Qwea1287!",
        )
        self.user.is_active = True
        self.user.email_confirmed = True
        self.user.save()
        self.data = {
            "email": "testuser@example.com",
            "password": "Qwea1287!",
        }

    def test_user_login(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
