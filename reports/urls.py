from django.urls import include, path
from .views import employee_pdf
urlpatterns = [path("holidays/", include("holidays.urls")), path("reports/employee/pdf/", employee_pdf)]
