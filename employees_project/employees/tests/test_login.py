from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee, Position


class LoginViewTestCase(APITestCase):

    def setUp(self):
        self.position = Position.objects.create(title='Team Leader')
        self.user = Employee.objects.create_user(
            email='user@example.com',
            password='password123',
            first_name='first_name',
            last_name='last_name',
            patronymic='patronymic',
            position=self.position,
            salary=100,
            total_paid=0,
        )

        self.valid_data = {
            "email": "user@example.com",
            "password": "password123"
        }

        self.nonexistent_email_in_data = {
            "email": "admin@admin.com",
            "password": "12345678"
        }

        self.invalid_password_in_data = {
            "email": "user@example.com",
            "password": "asfgdagertq34G4RKA"
        }

    def test_post_sign_in(self):
        url = reverse("log_in")

        response = self.client.post(url, data=self.valid_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post(url, data=self.nonexistent_email_in_data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        response = self.client.post(url, data=self.invalid_password_in_data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
