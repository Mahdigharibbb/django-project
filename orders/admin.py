from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
import openpyxl
from django.http import HttpResponse
# Register your models here.


def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spredsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=orders.xlsx'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Order"

    columns = ['آیدی', 'شماره تلفن', 'نام', 'نام خانوادگی', 'آدرس', 'کد پستی', 'شهر', 'وضعیت پرداخت', 'تاریخ خرید']
    ws.append(columns)

    for order in queryset:
        if order.created:
            if hasattr(order.created, 'strftime'):
                created = order.created.strftime('%Y-%m-%d %H:%M:%S')
            else:
                created = str(order.created)
        else:
            created = ''
        ws.append([
            order.id, order.buyer.phone, order.buyer.first_name, order.buyer.last_name, order.address.address,
            order.address.postal_code, order.address.city, order.paid, created
        ])
    wb.save(response)
    return response


export_to_excel.short_description = "خروجی اکسل"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'address', 'paid', 'created_jdate', 'updated_jdate']
    list_filter = ['paid', ('created', JDateFieldListFilter), ('updated', JDateFieldListFilter)]
    inlines = [OrderItemInline]
    actions = [export_to_excel]

    def created_jdate(self, obj):
        return obj.created.strftime('%Y/%m/%d ساعت:%H:%M')
    created_jdate.short_description = 'تاریخ ایجاد'

    def updated_jdate(self, obj):
        return obj.updated.strftime('%Y/%m/%d ساعت:%H:%M')
    updated_jdate.short_description = 'تاریخ ویرایش'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product']

