from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        ('KeepNet Profile Data', {'fields': ('bio', 'profile_picture')}),
    )