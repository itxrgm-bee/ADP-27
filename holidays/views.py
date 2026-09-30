from rest_framework import viewsets
from accounts.permissions import IsAdminRole
from .models import Holiday
from .serializers import HolidaySerializer
class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAdminRole]
    def perform_create(self, serializer): serializer.save(created_by=self.request.user)
