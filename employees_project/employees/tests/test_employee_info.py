from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from employees.models import Employee, Position


class UserInfoViewApiTestCase(APITestCase):
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

    def test_employee_info(self):
        url = reverse("employee_info")

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.email, response.json()["email"])
        self.assertEqual(self.user.first_name, response.json()["first_name"])
