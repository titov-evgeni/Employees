from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from employees.models import Employee, Position


class LogoutViewTestCase(APITestCase):

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

    def test_post_logout(self):
        url = reverse("log_out")
        refresh_token = str(RefreshToken().for_user(self.user))
        access_token = str(AccessToken().for_user(self.user))
        response = self.client.post(url, data={"refresh": refresh_token},
                                    HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
