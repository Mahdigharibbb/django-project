# Generated by Django 5.1.5 on 2025-03-21 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_shopuser_address_shopuser_default_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='default_address',
        ),
        migrations.AddField(
            model_name='shopuser',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
