from django.db import models
from datetime import datetime


# Create your models here.

# 用户模型
class UserInfo(models.Model):
    user_type_choics = (
        (1, "BD"),
        (2, "BDM"),
        (3, "CM"),
    )
    username = models.CharField(max_length=64, verbose_name="用户名")
    password = models.CharField(max_length=64, verbose_name="密码")
    user_type = models.IntegerField(choices=user_type_choics)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")

    class Mate:
        managed = True
        db_table = "user_info"
        verbose_name = "用户模型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 存放用户登录成功后的token
class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', unique=True, on_delete=False)
    token = models.CharField(max_length=64, verbose_name="用户token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Mate:
        managed = True
        db_table = "user_token"
        verbose_name = "用户Token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token
