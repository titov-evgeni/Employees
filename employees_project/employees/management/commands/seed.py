"""
Fill the database with random values
Use --mode=clear to clear all data without filling the database
"""
import random

from typing import Union
from django_seed import Seed
from django.core.management.base import BaseCommand

from employees.models import Employee, Position

"""Clear all data without filling the database"""
MODE_CLEAR = 'clear'

POSITIONS = ["Chief", "Team Leader", "Middle Manager", "Junior Manager",
             "Team Member"]


class Command(BaseCommand):
    help = "Fill the database with random values"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Fill the database')
        run_seed(options['mode'])
        self.stdout.write('Finished')


def clear_data():
    """Deletes all the table data"""
    Employee.objects.all().delete()
    Position.objects.all().delete()


def run_seed(mode: Union[None, str]) -> None:
    """
    Fill or clear database based on mode

    :param mode: database work method.
    str - if script run with argument --mode,
    None - if script run without this argument.
    :return: None
    """
    clear_data()
    if mode == MODE_CLEAR:
        return

    seeder = Seed.seeder()

    # Generation employees number on each level:
    employees_number = [level * 10 if level != 0 else 1 for level in range(Employee.HIERARCHY_LEVELS)]

    # Fill Position table
    for pos in POSITIONS:
        seeder.add_entity(Position, 1, {
            'title': pos,
        })
    seeder.execute()

    # Fill Employee table
    for level, count in enumerate(employees_number):
        for _ in range(count):
            first_name = seeder.faker.first_name()
            last_name = seeder.faker.last_name()
            patronymic = seeder.faker.last_name()
            if level == Employee.FIRST_LEVEL:
                chief = None
            else:
                chief = Employee.objects.filter(level=level - 1).order_by("?").first()
            employee_salary = random.randint(500, 3000)
            total_paid = random.randint(0, 10000)
            position = Position.objects.filter(title=random.choice(POSITIONS)).first()
            employment_date = seeder.faker.date_this_decade()
            email = f'{first_name}{employee_salary}@gmail.com'
            if Employee.objects.filter(email=email):
                email = 'my' + email
            employee = Employee(
                email=email,
                password="password123",
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                position=position,
                chief=chief,
                salary=employee_salary,
                employment_date=employment_date,
                total_paid=total_paid,
                level=level,
            )
            employee.save()
