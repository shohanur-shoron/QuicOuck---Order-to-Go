# Generated by Django 5.0.4 on 2024-04-28 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_avgreviewpoint_product_totalreviews'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
