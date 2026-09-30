from datetime import datetime, time
from ipaddress import ip_address
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from .models import Attendance, AttendanceAuditLog
from holidays.models import Holiday

class AttendanceError(Exception):
    def __init__(self, code, message): self.code, self.message = code, message

def client_ip(request):
    remote = request.META.get("REMOTE_ADDR", "")
    if remote in settings.TRUSTED_PROXY_IPS:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded: return forwarded.split(",")[0].strip()
    return remote

def ensure_network(request):
    detected = client_ip(request)
    try: allowed = any(ip_address(detected) == ip_address(value) for value in settings.ATTENDANCE_ALLOWED_IPS)
    except ValueError: allowed = False
    if not allowed: raise AttendanceError("ATTENDANCE_NETWORK_NOT_ALLOWED", "Check-in and check-out are only available from the authorized office network.")
    return detected

def workday_state(day):
    if day.weekday() == 6: return Attendance.Status.WEEKEND
    if Holiday.objects.filter(date=day).exists(): return Attendance.Status.HOLIDAY
    return None

def timing(now):
    configured = time.fromisoformat(settings.OFFICE_CHECK_IN_TIME)
    threshold = datetime.combine(now.date(), configured, tzinfo=now.tzinfo)
    minutes = max(0, int((now - threshold).total_seconds() // 60))
    late = minutes > settings.GRACE_PERIOD_MINUTES
    return late, minutes if late else 0

@transaction.atomic
def check_in(employee, request):
    ip = ensure_network(request); now = timezone.localtime()
    state = workday_state(now.date())
    if state == Attendance.Status.WEEKEND: raise AttendanceError("WEEKEND_ATTENDANCE_NOT_ALLOWED", "Attendance is unavailable on Sunday.")
    if state == Attendance.Status.HOLIDAY: raise AttendanceError("HOLIDAY_ATTENDANCE_NOT_ALLOWED", "Attendance is unavailable on a configured holiday.")
    attendance, created = Attendance.objects.select_for_update().get_or_create(employee=employee, attendance_date=now.date(), defaults={"status": Attendance.Status.PRESENT, "check_in_time": now, "check_in_ip": ip})
    if not created and attendance.check_in_time: raise AttendanceError("ALREADY_CHECKED_IN", "You have already checked in today.")
    late, minutes = timing(now); attendance.check_in_time, attendance.check_in_ip = now, ip; attendance.is_late, attendance.late_minutes = late, minutes; attendance.status = Attendance.Status.LATE if late else Attendance.Status.PRESENT; attendance.save()
    AttendanceAuditLog.objects.create(attendance=attendance, action=AttendanceAuditLog.Action.CHECK_IN, performed_by=employee, new_data={"check_in_time": now.isoformat(), "ip": ip}, ip_address=ip)
    return attendance

@transaction.atomic
def check_out(employee, request):
    ip = ensure_network(request); now = timezone.localtime()
    if workday_state(now.date()): raise AttendanceError("ATTENDANCE_NOT_ALLOWED", "Attendance is unavailable today.")
    try: attendance = Attendance.objects.select_for_update().get(employee=employee, attendance_date=now.date())
    except Attendance.DoesNotExist: raise AttendanceError("NOT_CHECKED_IN", "You must check in before checking out.")
    if attendance.check_out_time: raise AttendanceError("ALREADY_CHECKED_OUT", "You have already checked out today.")
    attendance.check_out_time, attendance.check_out_ip = now, ip; attendance.save()
    AttendanceAuditLog.objects.create(attendance=attendance, action=AttendanceAuditLog.Action.CHECK_OUT, performed_by=employee, new_data={"check_out_time": now.isoformat(), "ip": ip}, ip_address=ip)
    return attendance
