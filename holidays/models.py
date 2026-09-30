from django.conf import settings
from django.db import models
class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="holidays_created")
    class Meta: ordering = ("date",)
    def __str__(self): return f"{self.date}: {self.name}"
