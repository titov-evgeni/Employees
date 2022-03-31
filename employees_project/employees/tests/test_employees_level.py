from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from employees.models import Employee, Position


class EmployeeViewTestCase(APITestCase):
    def setUp(self):
        self.position = Position.objects.create(title='Team Leader')
        self.user1 = Employee.objects.create_user(
            email='user1@example.com',
            password='password123',
            first_name='first_name',
            last_name='last_name',
            patronymic='patronymic',
            employment_date="2022-03-30",
            position=self.position,
            salary=100,
            total_paid=0,
            level=1,
        )
        self.user2 = Employee.objects.create_user(
            email='user2@example.com',
            password='password123',
            first_name='first_name',
            last_name='last_name',
            patronymic='patronymic',
            employment_date="2022-03-30",
            position=self.position,
            chief=self.user1,
            level=1,
            salary=100,
            total_paid=0,
        )
        self.group = Group.objects.create(name='API Access')
        self.user1.groups.add(self.group.id)

    def test_employees(self):
        url = reverse("employees_level", kwargs={'level': 1})

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.json()), 2)

        url = reverse("employees_level", kwargs={'level': 2})
        response = self.client.get(url)
        self.assertEqual(len(response.json()), 0)
