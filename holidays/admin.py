from django.contrib import admin
from .models import Holiday
@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin): list_display=("date","name","created_by"); search_fields=("name",)
