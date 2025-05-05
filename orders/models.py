from django.db import models
from shop.models import Product, DiscountCode
from account.models import ShopUser, Address
import random
from django_jalali.db import models as jmodels


# Create your models here.


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('online', 'پرداخت آنلاین'),
        ('cod', 'پرداخت در محل'),
        ('bank', 'کارت به کارت'),
    ]
    buyer = models.ForeignKey(ShopUser, related_name='orders', on_delete=models.SET_NULL, null=True, verbose_name="شماره تلفن")
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="آدرس")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='online', verbose_name="محصول")
    discount_amount = models.PositiveIntegerField(default=0, verbose_name="کد تخفیف")
    final_price = models.PositiveIntegerField(default=0, verbose_name="قیمت آخر")
    delivery_code = models.CharField(max_length=12, unique=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="آپدیت شدن")
    paid = models.BooleanField(default=False, verbose_name="فعال")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    def __str__(self):
        return f"order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight <= 1000:
            return 20000
        elif 1000 <= weight >= 2000:
            return 30000
        else:
            return 50000

    def get_final_price(self):
        price = self.get_post_cost() + self.get_total_cost()
        return price

    def save(self, *args, **kwargs):
        if not self.delivery_code:
            self.delivery_code = self.generate_numeric_code()
        super().save(*args, **kwargs)

    def generate_numeric_code(self, length=8):
        while True:
            code = ''.join([str(random.randint(0, 9)) for _ in range(length)])
            if not Order.objects.filter(delivery_code=code).exists():
                return code


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE, verbose_name="محصول")
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    weight = models.PositiveIntegerField(default=0, verbose_name="وزن")
    discount_amount = models.PositiveIntegerField(default=0, verbose_name="کد تخفیف")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity

    # def get_total_price(self):
    #     # discount = self.discount_code.discount_amount if self.discount_code else 0
    #     # محاسبه قیمت کل این آیتم (محصول) با توجه به تعداد و قیمت هر محصول
    #     return self.get_cost() - self.discount_amount

    class Meta:
        verbose_name = "لیست سفارش"
        verbose_name_plural = "لیست سفارش ها"
