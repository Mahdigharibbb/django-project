from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

admin.sites.AdminSite.site_header = "پنل ادمین "
admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.index_title = "پنل مدیریت فروشگاه"


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class FeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'new_price', 'created_jdate', 'updated_jdate']

    prepopulated_fields = {'slug': ('name',)}
    list_filter = [('created', JDateFieldListFilter), ('updated', JDateFieldListFilter), 'inventory']
    inlines = [ImageInline, FeatureInline]

    def created_jdate(self, obj):
        return obj.created.strftime('%Y/%m/%d ساعت:%H:%M')
    created_jdate.short_description = 'تاریخ ایجاد'

    def updated_jdate(self, obj):
        return obj.updated.strftime('%Y/%m/%d ساعت:%H:%M')
    updated_jdate.short_description = 'تاریخ ویرایش'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'created_jdate', 'active']
    list_filter = ['active', ('created', JDateFieldListFilter), ('updated', JDateFieldListFilter)]
    search_fields = ['name', 'body']
    list_editable = ['active']
    # autocomplete_fields = ['post']

    def created_jdate(self, obj):
        return obj.created.strftime('%Y/%m/%d ساعت:%H:%M')
    created_jdate.short_description = 'تاریخ ایجاد'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['product', 'code', 'discount_amount', 'expiry_jdate', 'active']

    def expiry_jdate(self, obj):
        return obj.expiry_date.strftime('%Y/%m/%d ساعت:%H:%M')
    expiry_jdate.short_description = 'تاریخ انقضا'
