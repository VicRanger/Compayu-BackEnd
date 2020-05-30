# Generated by Django 3.0.4 on 2020-05-30 11:14

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('phonenum', models.CharField(max_length=11)),
                ('validcode', models.CharField(blank=True, max_length=255, null=True)),
                ('wxopenid', models.CharField(blank=True, max_length=255, null=True)),
                ('signup_type', models.CharField(blank=True, max_length=255, null=True)),
                ('is_signup', models.IntegerField(default=0)),
                ('signup_time', models.DateTimeField(blank=True, null=True)),
                ('signature', models.CharField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'UserProfile',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('media_type', models.CharField(blank=True, max_length=20, null=True)),
                ('picture', models.ImageField(blank=True, max_length=255, null=True, upload_to='pictures/%Y%m%d', verbose_name='图片')),
            ],
            options={
                'verbose_name': '媒体存储',
                'verbose_name_plural': '媒体存储',
                'db_table': 'Media',
            },
        ),
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('text', models.TextField()),
                ('type_raw', models.CharField(max_length=20)),
                ('type_ai', models.CharField(blank=True, max_length=20, null=True)),
                ('type_human', models.CharField(blank=True, max_length=20, null=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thought_author', to=settings.AUTH_USER_MODEL)),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thought_media', to='compayu.Media')),
            ],
            options={
                'verbose_name': '想法',
                'verbose_name_plural': '想法',
                'db_table': 'Thought',
            },
        ),
    ]
