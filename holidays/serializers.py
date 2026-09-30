from rest_framework import serializers
from .models import Holiday
class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ("id", "date", "name", "description", "created_at", "created_by")
        read_only_fields = ("id", "created_at", "created_by")
