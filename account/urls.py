from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name="login"),
    path('login/', views.login_view, name="login"),
    path('verify-code', views.verify_code, name='verify_code'),
    path('resend-verification-code/', views.resend_verification_code, name='resend_verification_code'),
    # path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('logout/', views.log_out, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/address/', views.profile_address, name="profile_address"),
    path('profile/likes/', views.profile_likes, name="profile_likes"),
    path('profile/history/', views.profile_history, name="profile_history"),
    path('profile/history/view/<int:id>', views.profile_history_view, name="profile_history_view"),
    path('set-default-address/', views.set_default_address, name="set_default_address"),

    path('password-reset/', views.password_reset_phone, name="password_reset_phone"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html', success_url='/account/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'), name="password_reset_complete"),

    path('register/', views.register, name="register"),

    path('remove_address', views.remove_address, name='remove_address'),

]
