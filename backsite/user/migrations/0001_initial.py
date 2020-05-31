
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
            options={
                'verbose_name': '邮箱验证信息',
                'db_table': 'EmailCode',
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
            options={
                'verbose_name': '手机号邮件发送记录',
                'db_table': 'PhoneAndEmailLog',
            },
        ),
        migrations.CreateModel(
            name='PhoneCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=25)),
                ('code', models.CharField(max_length=6)),
                ('generatedate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '手机号验证信息',
                'db_table': 'PhoneCode',
            },
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
                'db_table': 'User',
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
            options={
                'verbose_name': '用户Token',
                'verbose_name_plural': '用户Token',
                'db_table': 'UserToken',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserLoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(max_length=255)),
                ('logTime', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Login_set', to='user.User')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
                'db_table': 'UserLoginLog',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(default='这个家伙还没打算写自己的个性签名...', max_length=255)),
                ('gender', models.IntegerField(default='0')),
                ('birthday', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('registerinfo', models.CharField(default='000', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserInfo_set', to='user.User')),
            ],
            options={
                'verbose_name': '用户详细信息',
                'db_table': 'UserInfo',
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
                'db_table': 'Avatar',
            },
        ),
    ]
