# Generated by Django 5.0.2 on 2024-03-23 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.CharField(default='0', max_length=100),
        ),
    ]