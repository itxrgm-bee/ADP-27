from rest_framework import serializers
from .models import Attendance
class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="attendance_date")
    check_in = serializers.DateTimeField(source="check_in_time", format="%H:%M:%S", allow_null=True)
    check_out = serializers.DateTimeField(source="check_out_time", format="%H:%M:%S", allow_null=True)
    class Meta:
        model = Attendance
        fields = ("date", "check_in", "check_out", "status", "is_late", "late_minutes")
