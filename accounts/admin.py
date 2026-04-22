from django.contrib import admin
from .models import User, OTP, Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_verified')
    search_fields = ('email', 'phone')
    list_filter = ('is_verified',)

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'is_used', 'created_at')
    list_filter = ('is_used', 'created_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'address', 'created_at')
    search_fields = ('full_name',)


