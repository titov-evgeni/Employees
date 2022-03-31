"""
Fill the database with random values
Use --mode=clear to clear all data without filling the database
"""
import os
import psycopg2
import psycopg2.extensions
import random

from typing import Union

from django_seed import Seed
from django.core.management.base import BaseCommand

from employees.models import Employee, Position, User

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
        run_script(options['mode'])
        self.stdout.write('Finished')


def create_connection(db_name: str, db_user: str, db_password: str, 
                      db_host: str, db_port: str) -> Union[None, psycopg2.extensions.connection]:
    """
    Create connection to PostgreSQL database

    :param db_name: database name
    :param db_user: user name registered in Postgres
    :param db_password: user password
    :param db_host:
    :param db_port:
    :return: connection to database (psycopg2.extensions.connection class instance)
    :return: None - if connection is not possible
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except psycopg2.OperationalError as e:
        pass
    return connection


def execute_query(connection: psycopg2.extensions.connection,
                  query: str) -> None:
    """
    Execute send data query to the database

    :param connection: connection to database (psycopg2.extensions.connection class instance)
    :param query: data change query
    :return: None
    """
    connection.autocommit = True
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except psycopg2.OperationalError as e:
            pass


def execute_read_query(connection: psycopg2.extensions.connection,
                       query: str) -> None:
    """
    Execute read data query to the database

    :param connection: connection to database (psycopg2.extensions.connection class instance)
    :param query: read data query
    :return:
    """
    connection.autocommit = True
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except psycopg2.Error as e:
            pass


def clear_data(connection: psycopg2.extensions.connection) -> None:
    """
    Clean table in database

    :param connection: connection to database (psycopg2.extensions.connection class instance)
    :return: None
    """
    query = """
    BEGIN;
    TRUNCATE TABLE employees_employee CASCADE;
    TRUNCATE TABLE employees_position CASCADE;
    COMMIT;
    """
    execute_query(connection, query)


def run_script(mode: Union[None, str]) -> None:
    """
    Fill or clear database based on mode

    :param mode: database work method.
    str - if script run with argument --mode,
    None - if script run without this argument.
    :return: None
    """
    conn = create_connection(
        db_name=os.environ.get('POSTGRES_DB'),
        db_user=os.environ.get('POSTGRES_USER'),
        db_password=os.environ.get('POSTGRES_PASSWORD'),
        db_host=os.environ.get('POSTGRES_HOST'),
        db_port=os.environ.get('POSTGRES_PORT')
    )
    seeder = Seed.seeder()

    # Clear data from tables
    clear_data(conn)
    if mode == MODE_CLEAR:
        return

    # Generation employees number on each level:
    employees_number = [level * 10 if level != 0 else 1 for level in
                        range(Employee.HIERARCHY_LEVELS)]

    # Fill Position table
    query = """INSERT INTO employees_position (title)
    VALUES"""
    for pos in POSITIONS:
        query += f"\n('{pos}'),"
    query = query[:-1]
    execute_query(conn, query)

    for level, count in enumerate(employees_number):
        for _ in range(count):
            first_name = seeder.faker.first_name()
            last_name = seeder.faker.last_name()
            patronymic = seeder.faker.last_name()
            if level == Employee.FIRST_LEVEL:
                chief = "NULL"
            else:
                chief = Employee.objects.filter(level=level - 1).values("id").order_by("?").first()['id']
            employee_salary = random.randint(500, 3000)
            total_paid = random.randint(0, 10000)
            position = Position.objects.filter(title=random.choice(POSITIONS)).values("id").first()
            employment_date = seeder.faker.date_this_decade()
            password = 'password123'
            email = f'{first_name}{employee_salary}@gmail.com'
            if User.objects.filter(email=email):
                email = 'my' + email

            # Fill User table
            query = """INSERT INTO employees_user (email, password, is_superuser, is_staff, is_active) 
                VALUES"""
            query += (
                f"\n('{email}', '{password}', false, false, true)")
            execute_query(conn, query)

            # Fill Employee table
            user = User.objects.get(email=email).id
            query = """INSERT INTO employees_employee 
                (user_ptr_id, first_name, last_name, patronymic, position_id, employment_date, 
                salary, total_paid, chief_id, level) 
                VALUES"""
            query += (f"\n({user}, '{first_name}', '{last_name}', '{patronymic}', {position['id']}, "
                      f"'{employment_date}', '{employee_salary}', '{total_paid}', {chief}, '{level}')")
            execute_query(conn, query)
