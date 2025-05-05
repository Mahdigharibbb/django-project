from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django_jalali.db import models as jmodels
# Create your models here.


class ShopUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('You must provide a phone')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is staff must be true')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is superuser must be true')

        return self.create_user(phone, password, **extra_fields)


class ShopUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    first_name = models.CharField(max_length=25, verbose_name="نام")
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_staff = models.BooleanField(default=False, verbose_name="کارکنان")
    date_joined = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ عضویت")
    objects = ShopUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def get_addresses(self):
        return self.addresses.all()

    def get_default_address(self):
        return self.addresses.filter(is_default=True).first()

    def get_address(self):
        address = self.addresses.filter(is_default=True).first()
        return address.address if address else 'هنوز ادرسی ثبت نشده'

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"


class Address(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name="addresses", verbose_name="شماره تلفن")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="شماره تلفن")
    first_name = models.CharField(max_length=25, verbose_name="نام")
    city = models.CharField(max_length=100, verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    is_default = models.BooleanField(default=False, verbose_name="آدرس پیش فرض")

    def __str__(self):
        return f"{self.city} - {self.user.phone} - {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)

    def is_complete(self):
        return all([self.address, self.city, self.postal_code])

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
