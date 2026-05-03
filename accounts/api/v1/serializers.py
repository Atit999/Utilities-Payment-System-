from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile, OTP

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["email", "full_name", "address", "created_at"]
        read_only_fields = ["created_at"]


# -------------------------
# VERIFY OTP
# -------------------------
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        otp = OTP.objects.filter(
            user=user,
            code=data["code"],
            is_used=False
        ).order_by("-created_at").first()

        if not otp:
            raise serializers.ValidationError("Invalid OTP")

        if not otp.is_valid:
            raise serializers.ValidationError("OTP expired")

        # mark used
        otp.is_used = True
        otp.save()

        user.is_verified = True
        user.save()

        data["user"] = user
        return data


# -------------------------
# RESEND OTP
# -------------------------
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)