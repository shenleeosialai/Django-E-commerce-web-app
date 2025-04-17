# Generated by Django 5.1.7 on 2025-04-16 02:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_rename_coupons_coupon'),
        ('orders', '0004_order_coupon_order_discount'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='order',
            name='orders_orde_created_51311f_idx',
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='coupons.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created'], name='orders_orde_created_743fca_idx'),
        ),
    ]
