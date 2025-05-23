# Generated by Django 5.1.5 on 2025-04-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_address_alter_order_buyer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='discount_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='کد تخفیف'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='تعداد'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='weight',
            field=models.PositiveIntegerField(default=0, verbose_name='وزن'),
        ),
    ]
