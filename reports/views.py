from datetime import date
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdminRole
from accounts.models import User
from .pdf import attendance_pdf
from .services import report_rows, summary

def parse_dates(request):
    return date.fromisoformat(request.query_params["start_date"]), date.fromisoformat(request.query_params["end_date"])
@api_view(["GET"])
@permission_classes([IsAdminRole])
def employee_pdf(request):
    try: employee=User.objects.get(pk=request.query_params["employee_id"], role=User.Role.EMPLOYEE); start,end=parse_dates(request)
    except (User.DoesNotExist, KeyError, ValueError): return Response({"success":False,"error":"INVALID_PARAMETERS","message":"Invalid employee or date range."},status=400)
    rows=report_rows(employee,start,end); return FileResponse(attendance_pdf("Employee Attendance Report",employee,rows,summary(rows),f"{start} to {end}"),as_attachment=True,filename="employee-attendance.pdf")
