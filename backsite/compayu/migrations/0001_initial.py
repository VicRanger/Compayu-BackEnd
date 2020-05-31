# Generated by Django 3.0.3 on 2020-05-30 22:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wangeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', wangeditor.fields.WangRichTextField()),
            ],
            options={
                'verbose_name': '富文本',
                'verbose_name_plural': '富文本',
                'db_table': 'Editor',
            },
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
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thought_author', to='user.User')),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thought_media', to='compayu.Media')),
                ('rich_text', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thought_content', to='compayu.Editor')),
            ],
            options={
                'verbose_name': '想法',
                'verbose_name_plural': '想法',
                'db_table': 'Thought',
            },
        ),
    ]
