from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from accounts.models import Profile, OTP
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    OTPVerifySerializer,
    LoginSerializer,
)


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

        # create profile
        Profile.objects.create(
            user=user,
            full_name=self.request.data.get("full_name", "")
        )

        # generate OTP
        OTP.generate_otp(user)   # 👈 no duplication


# -------------------------
# VERIFY OTP
# -------------------------
class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = self.get_serializer().validate_and_get_user(request.data)

        return Response(jwt(user))


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