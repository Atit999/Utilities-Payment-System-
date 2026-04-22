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


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code  = serializers.CharField(max_length=6)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User email address")
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="User password"
    )