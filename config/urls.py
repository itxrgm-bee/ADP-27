from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/employees/", include("accounts.api_urls")),
    path("api/attendance/", include("attendance.urls")),
    path("api/admin/", include("reports.urls")),
    path("api/admin/", include("attendance.admin_urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("", include("dashboard.urls")),
]
