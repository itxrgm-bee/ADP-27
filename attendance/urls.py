from django.urls import path
from .views import employee_check_in, employee_check_out, my_attendance
urlpatterns = [path("check-in/", employee_check_in), path("check-out/", employee_check_out), path("my/", my_attendance)]
