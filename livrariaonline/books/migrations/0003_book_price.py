# Generated by Django 4.2.16 on 2024-09-11 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=8, verbose_name='Preço'),
        ),
    ]
