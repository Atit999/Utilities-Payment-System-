from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from accounts.models import Profile, OTP
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    OTPVerifySerializer,
    LoginSerializer,
    ResendOTPSerializer,
)

User = get_user_model()


# -------------------------
# JWT Helper
# -------------------------
def jwt(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


# -------------------------
# REGISTER
# -------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        Profile.objects.create(
            user=user,
            full_name=self.request.data.get("full_name", "")
        )

        OTP.generate_otp(user)


# -------------------------
# VERIFY OTP
# -------------------------
class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(jwt(user))


# -------------------------
# RESEND OTP (Swagger input ready)
# -------------------------
class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_verified:
            return Response(
                {"detail": "User already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        OTP.generate_otp(user)

        return Response(
            {"detail": "OTP sent successfully"},
            status=status.HTTP_200_OK
        )


# -------------------------
# LOGIN
# -------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = authenticate(
            email=data.validated_data["email"],
            password=data.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_verified:
            return Response(
                {"detail": "Verify your account first"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(jwt(user))


# -------------------------
# PROFILE
# -------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile