from django.contrib import admin
from calcprazo.models import *
from django.contrib.auth.admin import UserAdmin

class UserIAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username','email',  'password1', 'password2')
            }
        ),
    )

    list_display = ('username','email', 'is_active', 'is_staff', 'is_superuser')
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserIAdmin)

# Register your models here.
admin.site.register(Feriado)
admin.site.register(CalculaPrazo)
