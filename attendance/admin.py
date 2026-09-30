from django.contrib import admin
from .models import Attendance, AttendanceAuditLog
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display=("employee","attendance_date","status","check_in_time","check_out_time","manually_marked")
    readonly_fields=tuple(field.name for field in Attendance._meta.fields)
    def has_delete_permission(self, request, obj=None): return False
@admin.register(AttendanceAuditLog)
class AttendanceAuditLogAdmin(admin.ModelAdmin):
    list_display=("attendance","action","performed_by","timestamp"); readonly_fields=tuple(field.name for field in AttendanceAuditLog._meta.fields)
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False
