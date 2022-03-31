from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from employees.models import Employee, Position


class RegisterViewTestCase(APITestCase):
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
        self.group = Group.objects.create(name='API Access')
        self.user1.groups.add(self.group.id)

    def test_register(self):
        self.employee1_data = dict(
            email='user2@example.com',
            password='asdsa2dewr34eerf',
            confirm_password='asdsa2dewr34eerf',
            first_name='first_name',
            last_name='last_name',
            patronymic='patronymic',
            employment_date="2022-03-30",
            position=self.position.id,
            chief=self.user1.id,
            salary=100,
            total_paid=0,
        )
        url = reverse('register')

        response = self.client.get(url, data=self.employee1_data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(self.user1)
        response = self.client.post(url, data=self.employee1_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        expected_data = {
            "email": "user2@example.com",
            "first_name": "First_name",
            "last_name": "Last_name",
            "patronymic": "Patronymic",
            "position": self.position.id,
            "employment_date": "2022-03-30",
            "salary": "100.00",
            "total_paid": "0.00",
            "chief": self.user1.id,
            "level": 2,
            "groups": []
        }
        self.assertEqual(expected_data, response.data)
