# Generated by Django 5.0.4 on 2024-04-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='avgReviewPoint',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='product',
            name='totalReviews',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
