from datetime import date
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from accounts.models import User
from .models import Attendance
from .services import check_in, AttendanceError

@override_settings(ATTENDANCE_ALLOWED_IPS=["203.0.113.10"], TRUSTED_PROXY_IPS=["127.0.0.1"], OFFICE_CHECK_IN_TIME="09:00", GRACE_PERIOD_MINUTES=10)
class AttendanceServiceTests(TestCase):
    def setUp(self): self.employee=User.objects.create_user("0320-4644532", "password123", name="Ali")
    def request(self, headers=None):
        request=APIRequestFactory().post("/api/attendance/check-in/"); request.META["REMOTE_ADDR"]="203.0.113.10"; request.META.update(headers or {}); force_authenticate(request,user=self.employee); return request
    def test_phone_normalization_and_duplicate_check_in(self):
        self.assertEqual(self.employee.phone_number, "+923204644532")
        with override_settings(USE_TZ=True):
            from unittest.mock import patch
            from django.utils import timezone
            with patch("attendance.services.timezone.localtime", return_value=timezone.make_aware(__import__("datetime").datetime(2026,8,25,9,30))):
                check_in(self.employee,self.request())
                with self.assertRaises(AttendanceError) as error: check_in(self.employee,self.request())
                self.assertEqual(error.exception.code,"ALREADY_CHECKED_IN")
    def test_fake_forwarded_ip_is_ignored_from_untrusted_source(self):
        request=self.request({"HTTP_X_FORWARDED_FOR":"203.0.113.10"}); request.META["REMOTE_ADDR"]="198.51.100.9"
        with self.assertRaises(AttendanceError) as error: check_in(self.employee,request)
        self.assertEqual(error.exception.code,"ATTENDANCE_NETWORK_NOT_ALLOWED")
