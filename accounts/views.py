from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .permissions import IsAdminRole
from .serializers import EmployeeSerializer, LoginSerializer, UserSerializer

class LoginThrottle(AnonRateThrottle):
    scope = "login"

@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def login(request):
    serializer = LoginSerializer(data=request.data); serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]; refresh = RefreshToken.for_user(user)
    return Response({"success": True, "access": str(refresh.access_token), "refresh": str(refresh), "user": UserSerializer(user).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.data.get("refresh")
    if token:
        try: RefreshToken(token).blacklist()
        except Exception: pass
    return Response({"success": True, "message": "Logged out successfully."})

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET": return Response({"success": True, "user": UserSerializer(request.user).data})
    serializer = UserSerializer(request.user, data=request.data, partial=True); serializer.is_valid(raise_exception=True); serializer.save()
    return Response({"success": True, "user": serializer.data})

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=User.Role.EMPLOYEE).order_by("name")
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ["get", "post", "patch", "head", "options"]
