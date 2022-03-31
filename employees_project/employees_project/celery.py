import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employees_project.settings')
app = Celery('employees_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls pay_salary_task() every 2 hours.
    sender.add_periodic_task(crontab(minute=0, hour='*/2'), periodic_task.s('pay_salary'),
                             name='pay salary every 2 hours')

@app.task
def periodic_task(taskname):
    from employees.tasks import pay_salary_task

    if taskname == 'pay_salary':
        pay_salary_task()
