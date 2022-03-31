from django.urls import path

from employees.api.views import (
    EmployeeView,
    EmployeeLevelView,
    RegisterView,
    EmployeeInfoView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('', EmployeeView.as_view(), name='employees'),
    path('<int:level>/level/',
         EmployeeLevelView.as_view({'get': 'list'}), name='employees_level'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='log_in'),
    path('logout/', LogoutView.as_view(), name='log_out'),
    path('me/', EmployeeInfoView.as_view({'get': 'retrieve'}),
         name='employee_info'),
]
