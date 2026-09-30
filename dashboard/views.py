from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils import timezone
from accounts.models import User
from attendance.models import Attendance

def admin_required(user): return user.is_authenticated and user.role == User.Role.ADMIN
def dashboard(request):
    day=timezone.localdate(); rows=Attendance.objects.filter(attendance_date=day); return render(request,"dashboard/index.html",{"total_employees":User.objects.filter(role=User.Role.EMPLOYEE,is_active=True).count(),"present":rows.filter(status=Attendance.Status.PRESENT).count(),"late":rows.filter(status=Attendance.Status.LATE).count(),"incomplete":rows.filter(status=Attendance.Status.INCOMPLETE).count(),"working":rows.filter(check_in_time__isnull=False,check_out_time__isnull=True).count()})
dashboard= user_passes_test(admin_required, login_url="/django-admin/login/")(dashboard)
