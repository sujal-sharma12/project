# Generated by Django 5.0 on 2024-03-14 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='news/')),
                ('product', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
