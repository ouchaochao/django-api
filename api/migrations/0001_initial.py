# Generated by Django 2.0.5 on 2020-06-19 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('user_type', models.IntegerField(choices=[(1, '普通用户'), (2, '普通会员'), (3, '白金会员'), (4, '黄金会员')])),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='注册时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, verbose_name='用户token')),
                ('expiration_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='过期时间')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.OneToOneField(on_delete=False, to='api.UserInfo')),
            ],
        ),
    ]
