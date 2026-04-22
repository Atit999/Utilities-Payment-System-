from django.contrib import admin
from .models import Provider, Service, CustomerAccount


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ['name', 'code']
    list_filter = ['is_active']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'is_active')
    search_fields = ['name', 'provider__name']
    list_filter = ['provider', 'is_active']


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'account_number')
    search_fields = ['account_number', 'user__email']
    list_filter = ['service']