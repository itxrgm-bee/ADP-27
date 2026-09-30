from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import login, logout
urlpatterns = [path("login/", login), path("token/refresh/", TokenRefreshView.as_view()), path("logout/", logout)]
