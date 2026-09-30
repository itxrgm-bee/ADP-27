from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, me
router = DefaultRouter(); router.register("", EmployeeViewSet, basename="employee")
urlpatterns = [path("me/", me), path("", include(router.urls))]
