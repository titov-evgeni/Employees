from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from employees.models import Employee


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Employee
        fields = ('email',)


class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = ('email',)
