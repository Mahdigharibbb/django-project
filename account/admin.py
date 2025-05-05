from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm
from .forms import AddressForm

# Register your models here.


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    form = AddressForm
    list_display = ('user', 'first_name', 'city', 'is_default', 'phone', 'address')
    list_filter = ('user', 'is_default')
    search_fields = ('user__phone', 'city', 'postal_code')
    list_per_page = 20


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    ordering = ['phone']
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_default_address_display']
    readonly_fields = ['get_default_address_display']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'get_default_address_display')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'get_default_address_display')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_default_address_display(self, obj):
        default_address = obj.get_default_address()
        if default_address:
            return default_address.address
        return "آدرسی ثبت نشده"
    get_default_address_display.short_description = 'آدرس پیش فرض'
