from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, normalize_phone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "phone_number", "email", "designation", "role")

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        phone = normalize_phone(attrs["phone_number"])
        user = authenticate(phone_number=phone, password=attrs["password"])
        if not user:
            raise serializers.ValidationError({"code": "INVALID_CREDENTIALS", "message": "Invalid phone number or password."})
        if not user.is_active:
            raise serializers.ValidationError({"code": "ACCOUNT_DISABLED", "message": "This account is disabled."})
        attrs["user"] = user
        return attrs

class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    class Meta:
        model = User
        fields = ("id", "name", "phone_number", "email", "designation", "password", "role", "is_active", "created_at")
        read_only_fields = ("id", "role", "created_at")
    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, role=User.Role.EMPLOYEE, **validated_data)
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items(): setattr(instance, key, value)
        if password: instance.set_password(password)
        instance.save()
        return instance
