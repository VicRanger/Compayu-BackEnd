# Generated by Django 3.0.4 on 2020-05-26 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200526_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 26, 10, 30, 1, 801100)),
        ),
    ]
