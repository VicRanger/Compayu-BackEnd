# Generated by Django 3.0.4 on 2020-05-28 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200528_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='birthday',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 5, 28, 16, 34, 5, 261354)),
        ),
    ]
