from django.urls import path
from .views import manual_attendance
urlpatterns = [path("attendance/manual/", manual_attendance)]