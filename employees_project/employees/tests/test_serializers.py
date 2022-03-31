from django.test import TestCase

from employees.api.serializers import EmployeeSerializer, PositionSerializer
from employees.models import Employee, Position


class EmployeeSerializerTestCase(TestCase):

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

    def test_serialize(self):
        test_data1 = EmployeeSerializer(self.user1).data
        expected_data = {
            "id": self.user1.id,
            "email": "user1@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "position": 'Team Leader',
            "employment_date": "2022-03-30",
            "salary": "100.00",
            "total_paid": "0.00",
            "chief": None,
            "level": None,
            "groups": []
        }
        self.assertEqual(expected_data, test_data1)

        test_data2 = EmployeeSerializer(self.user2).data
        expected_data = {
            "id": self.user2.id,
            "email": "user2@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "patronymic": "patronymic",
            "position": 'Team Leader',
            "employment_date": "2022-03-30",
            "salary": "100.00",
            "total_paid": "0.00",
            "chief": "user1@example.com",
            "level": 1,
            "groups": []
        }
        self.assertEqual(expected_data, test_data2)


class PositionSerializerTestCase(TestCase):

    def setUp(self):
        self.position = Position.objects.create(title='Team Leader')

    def test_serialize(self):
        test_data = PositionSerializer(self.position).data
        expected_data = {
            "title": 'Team Leader',
        }
        self.assertEqual(expected_data, test_data)
