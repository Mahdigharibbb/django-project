from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class PhoneValidationMixin:
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise forms.ValidationError('شماره تلفن الزامی است')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط شامل اعداد باشد')

        if not phone.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود')

        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن باید 11 رقم باشد')

        user_qs = ShopUser.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            user_qs = user_qs.exclude(pk=self.instance.pk)

        if user_qs.exists():
            raise forms.ValidationError('شماره تلفن قبلاً در سیستم ثبت شده است')

        return phone


class ShopUserCreationForm(UserCreationForm, PhoneValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


class ShopUserChangeForm(UserChangeForm, PhoneValidationMixin):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


class UserRegisterForm(forms.ModelForm, PhoneValidationMixin):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}), label='شماره تلفن')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='پسورد')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='تکرار پسورد')

    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("پسورد ها مطابقت ندارند!")

        return cleaned_data


class UserEditForm(forms.ModelForm, PhoneValidationMixin):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name']


class ProfileEditForm(forms.ModelForm, PhoneValidationMixin):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['phone', 'first_name', 'city', 'address', 'postal_code', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_default'].required = False
    def set_user(self, user):
        self.user = user

    def clean_is_default(self):
        """Ensure only one default address exists."""
        is_default = self.cleaned_data.get('is_default')
        user = self.instance.user

        if is_default:
            Address.objects.filter(user=user).exclude(id=self.instance.id).update(is_default=False)

        return is_default
