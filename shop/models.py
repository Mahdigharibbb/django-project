from django.db import models
from django.urls import reverse
from account.models import ShopUser
from django_jalali.db import models as jmodels

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="نام دسته بندی")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="اسلاگ")

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='دسته بندی')
    name = models.CharField(max_length=255, verbose_name='نام')
    slug = models.SlugField(max_length=255, verbose_name='اسلاگ')
    description = models.TextField(max_length=1200, verbose_name='توضیحات')
    inventory = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    weight = models.PositiveIntegerField(default=0, verbose_name='وزن')
    off = models.PositiveIntegerField(default=0, verbose_name='تخفیف', null=False, blank=False)
    new_price = models.PositiveIntegerField(default=0, verbose_name='قیمت پس از تخفیف')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')
    likes = models.ManyToManyField(ShopUser, related_name="liked_products", blank=True)
    total_likes = models.PositiveIntegerField(default=0)

    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]

        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_in_product(self):
        return reverse('shop:product_list_in_id', args=[self.id])

    def get_off(self):
        if self.new_price and self.new_price < self.price:
            return self.price - self.new_price
        return '10'

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    file = models.ImageField(upload_to="post_images/%Y/%m/%d")
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصویر ها"


class ProductFeature(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام ویژگی')
    value = models.CharField(max_length=255, verbose_name='مقدار ویژگی')
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE, verbose_name='محصول ها')

    def __str__(self):
        return self.name + ":" + self.value


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", verbose_name="محصول")
    name = models.CharField(max_length=100, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}: {self.product}"


class Ticket(models.Model):
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(max_length=250, verbose_name="موضوع")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.subject


class DiscountCode(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="discount_codes", default=1, verbose_name="محصول")  # مرتبط با محصول خاص
    code = models.CharField(max_length=50, unique=True, verbose_name="کد تخفیف")  # کد تخفیف
    discount_amount = models.PositiveIntegerField(default=0, verbose_name='مقدار تخفیف')
    active = models.BooleanField(default=True, verbose_name="فعال")  # آیا کد تخفیف فعال است؟
    expiry_date = jmodels.jDateTimeField(null=True, blank=True, verbose_name="تاریخ انقضا")  # تاریخ انقضا (اختیاری)

    def __str__(self):
        return f"{self.code} - {self.discount_amount} تومان"

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کد تخفیف ها"