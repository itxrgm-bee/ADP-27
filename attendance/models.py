from django.conf import settings
from django.db import models
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT="PRESENT","Present"; LATE="LATE","Late"; ABSENT="ABSENT","Absent"; HOLIDAY="HOLIDAY","Holiday"; WEEKEND="WEEKEND","Weekend"; LEAVE="LEAVE","Leave"; INCOMPLETE="INCOMPLETE","Incomplete"
    class Source(models.TextChoices): EMPLOYEE="EMPLOYEE","Employee"; ADMIN="ADMIN","Admin"
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attendance")
    attendance_date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)
    is_late = models.BooleanField(default=False)
    late_minutes = models.PositiveIntegerField(default=0)
    check_in_ip = models.GenericIPAddressField(null=True, blank=True)
    check_out_ip = models.GenericIPAddressField(null=True, blank=True)
    check_in_source = models.CharField(max_length=10, choices=Source.choices, default=Source.EMPLOYEE)
    check_out_source = models.CharField(max_length=10, choices=Source.choices, default=Source.EMPLOYEE)
    manually_marked = models.BooleanField(default=False)
    manual_reason = models.CharField(max_length=255, blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="manual_attendance")
    created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=("employee", "attendance_date"), name="unique_employee_attendance_date")]
        indexes = [models.Index(fields=("employee", "attendance_date")), models.Index(fields=("attendance_date",)), models.Index(fields=("status",)), models.Index(fields=("manually_marked",))]
    def __str__(self): return f"{self.employee} - {self.attendance_date}"

class AttendanceAuditLog(models.Model):
    class Action(models.TextChoices): CHECK_IN="CHECK_IN","Check in"; CHECK_OUT="CHECK_OUT","Check out"; MANUAL_CREATE="MANUAL_CREATE","Manual create"
    attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT, related_name="audit_logs")
    action = models.CharField(max_length=20, choices=Action.choices)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    old_data = models.JSONField(default=dict); new_data = models.JSONField(default=dict)
    reason = models.TextField(blank=True); ip_address = models.GenericIPAddressField(null=True, blank=True); timestamp = models.DateTimeField(auto_now_add=True)
