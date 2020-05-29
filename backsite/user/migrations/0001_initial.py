# Generated by Django 3.0.4 on 2020-05-29 21:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('code', models.CharField(max_length=6)),
                ('generatedate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('media_id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('media_type', models.CharField(blank=True, max_length=20, null=True)),
                ('picture', models.ImageField(blank=True, max_length=255, null=True, upload_to='pictures/%Y%m%d', verbose_name='图片')),
            ],
            options={
                'verbose_name': '媒体存储',
                'verbose_name_plural': '媒体存储',
            },
        ),
        migrations.CreateModel(
            name='PhoneAndEmailLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('phone', models.CharField(blank=True, max_length=25)),
                ('email', models.CharField(blank=True, max_length=25)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('log', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=25)),
                ('code', models.CharField(max_length=6)),
                ('generatedate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('phonenum', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=255)),
                ('wxopenid', models.CharField(blank=True, max_length=255, null=True)),
                ('signup_type', models.CharField(blank=True, max_length=255, null=True)),
                ('signup_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('password', models.CharField(max_length=255)),
                ('lastlogin', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(default='https://cdn.wzz.ink/avatar/defaultAvatar.png', max_length=512, upload_to='')),
                ('userType', models.CharField(default='普通用户', max_length=25)),
                ('level', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100, verbose_name='用户token')),
                ('expiration_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='过期时间')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Usertoken_set', to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(default='这个家伙还没打算写自己的个性签名...', max_length=255)),
                ('gender', models.IntegerField(default='0')),
                ('birthday', models.DateField(blank=True, default=datetime.datetime(2020, 5, 29, 21, 29, 40, 856651))),
                ('modified', models.DateTimeField(auto_now=True)),
                ('registerinfo', models.CharField(default='000', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserInfo_set', to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('thought_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40)),
                ('text', models.TextField()),
                ('type_raw', models.CharField(max_length=20)),
                ('type_ai', models.CharField(blank=True, max_length=20, null=True)),
                ('type_human', models.CharField(blank=True, max_length=20, null=True)),
                ('create_time', models.DateTimeField()),
                ('modified_time', models.DateTimeField(blank=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thought_author', to='user.User')),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thought_media', to='user.Media')),
            ],
            options={
                'verbose_name': '想法',
                'verbose_name_plural': '想法',
            },
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('media_id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('media_type', models.CharField(blank=True, max_length=20, null=True)),
                ('picture', models.ImageField(blank=True, max_length=255, null=True, upload_to='avatar/%Y%m%d', verbose_name='头像')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Avatar_set', to='user.User')),
            ],
            options={
                'verbose_name': '头像',
                'verbose_name_plural': '头像',
            },
        ),
    ]
