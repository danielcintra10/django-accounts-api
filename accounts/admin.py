from django.contrib import admin
from .models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'country', 'city', 'address', 'mobile_phone', 'is_active', ]
    list_filter = ['first_name', 'last_name', 'email', 'country', ]


admin.site.register(User, UserAdmin)
