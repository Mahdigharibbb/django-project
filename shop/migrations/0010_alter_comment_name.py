# Generated by Django 5.1.5 on 2025-03-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
    ]
