from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from .models import *
from .forms import *
from orders.models import Order, OrderItem
from shop.forms import *
from common.KaveSms import *
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            tokens = ''.join(random.choices('0123456789', k=6))
            request.session['verification_code'] = tokens
            request.session['phone'] = phone

            expiration_time = timezone.now() + timedelta(minutes=1)
            request.session['verification_code_expiration'] = expiration_time.isoformat()
            # print(tokens)
            send_sms_with_template(phone, tokens)

            return redirect('account:verify_code')
        else:
            messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است.')
    return render(request, 'registration/login.html')


def verify_code(request):
    context = {}

    expiration_time_str = request.session.get('verification_code_expiration')
    if expiration_time_str:
        context['expiration_time'] = expiration_time_str
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            expiration_time_str = request.session.get('verification_code_expiration')

            if expiration_time_str:
                if expiration_time_str.endswith('Z'):
                    expiration_time_str = expiration_time_str[:-1] + '+00:00'
                expiration_time = timezone.datetime.fromisoformat(expiration_time_str)
                if timezone.now() > expiration_time:
                    messages.error(request, 'کد تایید منقضی شده است. لطفاً دوباره درخواست دهید.')
                    return redirect('account:login')

            if code == verification_code:
                try:
                    user = ShopUser.objects.get(phone=phone)
                    login(request, user)
                    del request.session['verification_code']
                    del request.session['phone']
                    del request.session['verification_code_expiration']
                    return redirect('account:profile')
                except ShopUser.DoesNotExist:
                    messages.error(request, 'کاربری با این شماره یافت نشد.')
            else:
                messages.error(request, 'کد اشتباه')
    return render(request, 'registration/verify_code.html', context)


def resend_verification_code(request):
    if request.method == 'POST':
        phone = request.session.get('phone')
        if not phone:
            return JsonResponse({'success': False, 'error': 'شماره تماس یافت نشد.'})

        new_code = ''.join(random.choices('0123456789', k=6))
        # print(f"کد جدید: {new_code}")
        send_sms_with_template(phone, new_code)

        new_expiration_time = 60
        new_expiration = timezone.now() + timedelta(seconds=new_expiration_time)

        request.session['verification_code'] = new_code
        request.session['verification_code_expiration'] = new_expiration.isoformat()

        return JsonResponse({
            'success': True,
            'new_expiration_time': new_expiration_time
        })
    return JsonResponse({'success': False})


@login_required
def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    user = request.user
    try:
        address = Address.objects.get(user=user, is_default=True)
    except Address.DoesNotExist:
        address = Address.objects.create(user=user, is_default=True)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        account_form = ProfileEditForm(request.POST, request.FILES, instance=user)
        address_form = AddressForm(request.POST, instance=address)

        if account_form.is_valid() and user_form.is_valid() and address_form.is_valid():
            if user_form.has_changed() or account_form.has_changed() or address_form.has_changed():
                account_form.save()
                user_form.save()
                address = address_form.save(commit=False)
                address.user = user
                address.is_default = True
                if address.is_default:
                    Address.objects.filter(user=user).exclude(id=address.id).update(is_default=False)
                address.save()
                messages.success(request, "اطلاعات شما با موفقیت تغییر کرد.")
        else:
            messages.error(request, "لطفاً اطلاعات را درست وارد کنید.")
    else:
        user_form = UserEditForm(instance=user)
        account_form = UserEditForm(instance=user)
        address_form = AddressForm(instance=address)

    context = {
        'account_form': account_form,
        'user_form': user_form,
        'address_form': address_form,
        'user': user
    }
    return render(request, 'account/profile.html', context)


def set_default_address(request):
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)

            Address.objects.filter(user=request.user).update(is_default=False)

            address.is_default = True
            address.save()

            return JsonResponse({"success": True, "address_id": address.id})

    return JsonResponse({"success": False})


@login_required
def profile_address(request):
    addresses = Address.objects.filter(user=request.user)
    if request.method == "POST":
        address_id = request.POST.get("address_id")

        if address_id:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            form = AddressForm(request.POST, instance=address)
            form.set_user(request.user)
        else:
            form = AddressForm(request.POST)
            form.instance.user = request.user

        if form.is_valid():
            form.save()
            if address_id:
                messages.success(request, "آدرس با موفقیت ویرایش شد!")
            else:
                messages.success(request, "آدرس با موفقیت ثبت شد!")
            return redirect('account:profile_address')
        else:
            messages.error(request, "مشکلی در ذخیره آدرس وجود دارد. لطفاً فرم را بررسی کنید.")

    else:
        form = AddressForm()
    context = {
        'addresses': addresses,
        'form': form
    }
    return render(request, 'account/profile-address.html', context)


def remove_address(request):
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        try:
            address = get_object_or_404(Address, id=address_id)
            address.delete()

            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False, 'error': 'آیتم پیدا نشد'})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'})


def profile_likes(request):
    liked_products = Product.objects.filter(likes=request.user)
    context = {
        'liked_products': liked_products,
    }
    return render(request, 'account/profile-likes.html', context)


def profile_history(request):
    user = request.user
    orders = Order.objects.filter(buyer=user).order_by('-created')
    return render(request, 'account/profile-history.html', {'orders': orders})


def profile_history_view(request, id):
    order = Order.objects.get(id=id)
    context = {
        'order': order,
    }
    return render(request, 'account/profile-history-view.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register-done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def password_reset_phone(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        try:
            user = ShopUser.objects.get(phone=phone)
        except ShopUser.DoesNotExist:
            return HttpResponse("کاربری با این شماره موبایل یافت نشد.", status=400)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(reverse('account:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        print(f"🔗 لینک بازنشانی رمز عبور برای شماره {phone}: {reset_link}")

        send_sms_with_template(phone, reset_link, template='resetpasslink', is_link=True)

        return redirect('account:password_reset_done')

    return render(request, "registration/password_reset_form.html")
