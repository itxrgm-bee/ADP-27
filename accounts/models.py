from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^\+?[0-9]{10,15}$", "Enter a valid phone number.")

def normalize_phone(value):
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if digits.startswith("92") and len(digits) == 12:
        return "+" + digits
    if digits.startswith("0") and len(digits) == 11:
        return "+92" + digits[1:]
    return "+" + digits if not str(value).strip().startswith("+") else "+" + digits

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number: raise ValueError("Phone number is required")
        user = self.model(phone_number=normalize_phone(phone_number), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.update(is_staff=True, is_superuser=True, role=User.Role.ADMIN)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYEE = "EMPLOYEE", "Employee"
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=16, unique=True, validators=[phone_validator])
    email = models.EmailField(blank=True)
    designation = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.EMPLOYEE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()
    def save(self, *args, **kwargs):
        self.phone_number = normalize_phone(self.phone_number)
        super().save(*args, **kwargs)
    def __str__(self): return f"{self.name} ({self.phone_number})"
