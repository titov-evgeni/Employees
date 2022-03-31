from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employees.models import Employee, Position, User
from employees.tasks import delete_total_paid_task
from employees.forms import EmployeeCreationForm, EmployeeChangeForm


def delete_total_paid(modeladmin, request, queryset):
    """Remove all information on the paid wages of all selected employees"""
    if len(queryset) >= 20:
        delete_total_paid_task.delay((list(queryset.values_list('id', flat=True))))
    else:
        queryset.update(total_paid=0)


delete_total_paid.short_description = 'Delete total paid wages'


class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    list_display = ('first_name', 'last_name', 'patronymic',
                    'position', 'chief', 'salary', 'total_paid',
                    )
    list_display_links = ('first_name', 'chief',)
    list_filter = ('position', 'level',)
    actions = (delete_total_paid,)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name',
                           'patronymic', 'position', 'employment_date',
                           'salary', 'total_paid', 'chief', 'level')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',
                           'patronymic', 'position', 'employment_date',
                           'salary', 'total_paid', 'chief', 'level')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Employee, EmployeeAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


admin.site.register(Position, PositionAdmin)
admin.site.register(User)
