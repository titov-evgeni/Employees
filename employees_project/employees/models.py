from datetime import date
from typing import Union
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator

from employees.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, name='email')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.email}'


class Employee(User):
    """Model for defining employees"""

    FIRST_LEVEL = 0
    HIERARCHY_LEVELS = 5  # from 0 to 4 level
    LAST_LEVEL = HIERARCHY_LEVELS - 1

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    position = models.ForeignKey('Position', on_delete=models.PROTECT)
    employment_date = models.DateField(default=date.today)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    chief = models.ForeignKey('self', on_delete=models.SET_NULL,
                              blank=True, null=True)
    level = models.PositiveIntegerField(validators=[MaxValueValidator(LAST_LEVEL)],
                                        blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def check_possibility_of_having_subordinates(self):
        """
        Check employee possibility of having subordinates

        :return: employee level - if employee can have subordinates
        :return: None - if employee cannot have subordinates
        """
        if self.level == self.LAST_LEVEL:
            return None
        return self.level


class Position(models.Model):
    """Model for defining employees positions"""

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
