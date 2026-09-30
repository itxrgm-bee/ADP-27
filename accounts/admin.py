from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class EmployeeAdmin(UserAdmin):
    model = User
    list_display = ("name", "phone_number", "designation", "role", "is_active")
    ordering = ("name",)
    fieldsets = ((None, {"fields": ("phone_number", "password")}), ("Personal", {"fields": ("name", "email", "designation")}), ("Access", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}))
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("phone_number", "name", "password1", "password2", "role", "is_active")}),)
    search_fields = ("name", "phone_number")
