from datetime import date, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Attendance
from .permissions import IsEmployee
from .serializers import AttendanceSerializer
from .services import AttendanceError, check_in, check_out, workday_state
from accounts.permissions import IsAdminRole
from .models import AttendanceAuditLog

def error_response(error): return Response({"success": False, "error": error.code, "message": error.message, "details": {}}, status=400)
@api_view(["POST"])
@permission_classes([IsEmployee])
def employee_check_in(request):
    try: record = check_in(request.user, request)
    except AttendanceError as error: return error_response(error)
    return Response({"success": True, "message": "Check-in successful", "attendance": AttendanceSerializer(record).data})
@api_view(["POST"])
@permission_classes([IsEmployee])
def employee_check_out(request):
    try: record = check_out(request.user, request)
    except AttendanceError as error: return error_response(error)
    return Response({"success": True, "message": "Check-out successful", "attendance": AttendanceSerializer(record).data})

def parse_range(request):
    try:
        end = date.fromisoformat(request.query_params.get("end_date") or request.query_params.get("date") or str(date.today()))
        start = date.fromisoformat(request.query_params.get("start_date") or request.query_params.get("date") or str(end))
    except ValueError: raise ValueError
    if start > end or (end - start).days > 366: raise ValueError
    return start, end
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_attendance(request):
    try: start, end = parse_range(request)
    except ValueError: return Response({"success": False, "error": "INVALID_DATE_RANGE", "message": "Provide a valid date range of at most one year.", "details": {}}, status=400)
    records = {item.attendance_date: item for item in Attendance.objects.filter(employee=request.user, attendance_date__range=(start, end))}
    rows=[]; counts={key: 0 for key in ("PRESENT", "LATE", "ABSENT", "HOLIDAY", "WEEKEND")}
    day=start
    while day <= end:
        item=records.get(day); status=item.status if item else workday_state(day) or Attendance.Status.ABSENT
        if item: data=AttendanceSerializer(item).data
        else: data={"date": day, "check_in": None, "check_out": None, "status": status, "is_late": False, "late_minutes": 0}
        rows.append(data); counts[status]=counts.get(status, 0)+1; day += timedelta(days=1)
    return Response({"success": True, "summary": {"total_days": len(rows), "present_days": counts.get("PRESENT",0), "late_days": counts.get("LATE",0), "absent_days": counts.get("ABSENT",0), "holiday_days": counts.get("HOLIDAY",0), "weekend_days": counts.get("WEEKEND",0)}, "attendance": rows})

@api_view(["POST"])
@permission_classes([IsAdminRole])
def manual_attendance(request):
    from accounts.models import User
    from django.utils.dateparse import parse_date, parse_datetime
    employee = User.objects.filter(pk=request.data.get("employee_id"), role=User.Role.EMPLOYEE).first()
    day = parse_date(request.data.get("date", "")); check_in_value = parse_datetime(request.data.get("check_in", ""))
    if not employee or not day or not check_in_value or not request.data.get("reason"):
        return Response({"success": False, "error": "INVALID_PARAMETERS", "message": "Employee, date, check-in and reason are required.", "details": {}}, status=400)
    if Attendance.objects.filter(employee=employee, attendance_date=day).exists():
        return Response({"success": False, "error": "ATTENDANCE_EXISTS", "message": "Existing attendance cannot be overwritten.", "details": {}}, status=409)
    check_out_value = parse_datetime(request.data.get("check_out", "")) if request.data.get("check_out") else None
    record = Attendance.objects.create(employee=employee, attendance_date=day, check_in_time=check_in_value, check_out_time=check_out_value, status=Attendance.Status.PRESENT, check_in_source=Attendance.Source.ADMIN, check_out_source=Attendance.Source.ADMIN, manually_marked=True, manual_reason=request.data["reason"], marked_by=request.user)
    AttendanceAuditLog.objects.create(attendance=record, action=AttendanceAuditLog.Action.MANUAL_CREATE, performed_by=request.user, reason=request.data["reason"], new_data={"date": str(day), "check_in": str(check_in_value), "check_out": str(check_out_value)}, ip_address=request.META.get("REMOTE_ADDR"))
    return Response({"success": True, "message": "Manual attendance created.", "attendance": {"id": record.id, "date": day, "status": record.status}}, status=201)
