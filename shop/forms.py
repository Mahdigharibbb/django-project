from django import forms
from .models import *


class SearchForm(forms.Form):
    query = forms.CharField()


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه است")
            else:
                return name

    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'متن',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'نام',
                'class': 'form-control'
            }),
        }
        error_messages = {
            'name': {
                'required': "لطفاً عنوان نظر خود را وارد کنید.",
                'max_length': "عنوان نظر نمی‌تواند بیشتر از 100 کاراکتر باشد.",
            },
            'body': {
                'required': "متن نظر نمی‌تواند خالی باشد.",
                'max_length': "متن نظر نباید بیشتر از 500 کاراکتر باشد.",
            }
        }


class DiscountForm(forms.Form):
    discount_code = forms.CharField(max_length=50, required=True, label="کد تخفیف")
    product_id = forms.IntegerField(required=True, widget=forms.HiddenInput())  # شناسه محصول


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError('شماره تلفن الزامی است')

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط شامل اعداد باشد')

        if not phone.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود')

        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن باید 11 رقم باشد')

        return phone

