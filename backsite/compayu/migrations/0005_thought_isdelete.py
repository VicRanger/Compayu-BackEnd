# Generated by Django 3.0.4 on 2020-06-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compayu', '0004_remove_thought_viewtimes'),
    ]

    operations = [
        migrations.AddField(
            model_name='thought',
            name='isdelete',
            field=models.BooleanField(default=False),
        ),
    ]