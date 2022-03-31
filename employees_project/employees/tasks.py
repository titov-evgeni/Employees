from celery import shared_task
from django.db.models import F

from employees.models import Employee


@shared_task
def delete_total_paid_task(queryset):
    """Remove all information on the paid wages of all selected employees"""
    Employee.objects.filter(id__in=queryset).update(total_paid=0)


@shared_task
def pay_salary_task():
    """Pay employees salary"""
    Employee.objects.update(total_paid=F('total_paid')+F('salary'))

