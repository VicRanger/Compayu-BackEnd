import os
from datetime import datetime

# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from backsite.settings import MEDIA_ROOT

'''# 用户表，基础表
class User(models.Model):
    objects = models.manager
    # 会有自带的ID

    # 用户姓名
    username = models.CharField(max_length=20)
    # 密码
    passwd = models.CharField(max_length=255)
    # 昵称
    nickname = models.CharField(max_length=25)
    # 电话
    phonenum = models.CharField(max_length=20, blank=True)
    # 邮箱
    email = models.EmailField(max_length=50, blank=True)
    # 微信openid
    wxopenid = models.CharField(max_length=20, blank=True)
    # 注册方式
    registertype = models.CharField(max_length=10)  # wechat/phonenum/email
    # 上次登录时间
    lastlogindate = models.DateTimeField()
    # 注册时间
    registerdate = models.DateTimeField(auto_now=True)'''

class User(models.Model):
    objects = models.manager

    nickname = models.CharField(max_length=255, blank=True, null=True)
    phonenum = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)
    wxopenid = models.CharField(max_length=255, blank=True, null=True)
    signup_type = models.CharField(max_length=255, blank=True, null=True)
    signup_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    lastlogin = models.DateTimeField(auto_now=True)
    #默认头像 'https://cdn.wzz.ink/avatar/defaultAvatar.png'
    avatar = models.ImageField(max_length=512, default=os.path.join(MEDIA_ROOT, 'avatar/defaultAvatar.png'))
    userType = models.CharField(max_length=25, default="普通用户")
    level = models.IntegerField(default=1)

    class Meta:
        db_table = 'User'  # 自己设计表名
        verbose_name='用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname

# 用户详细信息表
class UserInfo(models.Model):
    objects = models.manager
    # 会有自带的ID

    # 个性签名
    signature = models.CharField(max_length=255, default="这个家伙还没打算写自己的个性签名...")
    # 用户ID外键
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserInfo_set')
    # 性别，1-male  2-famale 0-unknown
    gender = models.IntegerField(default='0')
    # 生日
    birthday = models.DateField(blank=True, auto_now_add=True)
    # 更新时间
    modified = models.DateTimeField(auto_now=True)
    # 信息完整度 “10“-email "11:-email and phone之类的
    registerinfo = models.CharField(max_length=2, default="000")
    class Meta:
        db_table = 'UserInfo'  # 自己设计表名
        verbose_name='用户详细信息'

class EmailCode(models.Model):
    objects = models.manager
    # 会有自带的ID
    # 用户邮箱
    email = models.EmailField(max_length=255)
    # 随机生成的验证码
    code = models.CharField(max_length=6)
    # 生成日期
    generatedate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'EmailCode'  # 自己设计表名
        verbose_name='邮箱验证信息'

class PhoneCode(models.Model):
    objects = models.manager
    # 自带的ID
    # 用户注册用的手机号
    phone = models.CharField(max_length=25)
    # 随机生成的验证码
    code = models.CharField(max_length=6)
    # 生成的日期
    generatedate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'PhoneCode'  # 自己设计表名
        verbose_name='手机号验证信息'

# 用来记录发送验证码邮件和短信的数据
class PhoneAndEmailLog(models.Model):
    objects = models.manager
    # 自带的ID
    # 方式
    type = models.CharField(max_length=10)  # 'phone' or 'email'
    # 号码
    phone = models.CharField(max_length=25, blank=True)
    # 邮件
    email = models.CharField(max_length=25, blank=True)
    # 日期
    date = models.DateTimeField(auto_now_add=True)
    # 日志
    log = models.CharField(max_length=255)
    class Meta:
        db_table = 'PhoneAndEmailLog'  # 自己设计表名
        verbose_name='手机号邮件发送记录'

class UserToken(models.Model):
    objects = models.manager

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Usertoken_set')
    token = models.CharField(max_length=100, verbose_name="用户token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        managed = True
        db_table = "UserToken"
        verbose_name = "用户Token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token


# 头像
class Avatar(models.Model):
    objects = models.manager
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Avatar_set')
    media_id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    media_type = models.CharField(max_length=20, blank=True, null=True)
    picture = models.ImageField(blank=True,
                                        null=True,
                                        upload_to="avatar/%Y%m%d",
                                        max_length=255,
                                        verbose_name="头像")

    class Meta:
        db_table = "Avatar"
        verbose_name='头像'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.link, self.media_type)


# class User(models.Model):
#     objects = models.manager
#
#     nickname = models.CharField(max_length=255, blank=True, null=True)
#     phonenum = models.CharField(max_length=11)
#     email = models.EmailField(max_length=255)
#     wxopenid = models.CharField(max_length=255, blank=True, null=True)
#     signup_type = models.CharField(max_length=255, blank=True, null=True)
#     signup_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     password = models.CharField(max_length=255)
#     lastlogin = models.DateTimeField(auto_now=True)
#     avatar = models.ImageField(max_length=512, default=os.path.join(MEDIA_ROOT, 'avatar/defaultAvatar.png'))
#     userType = models.CharField(max_length=25, default="普通用户")
#     level = models.IntegerField(default=1)
#
#     class Meta:
#         verbose_name='用户'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.nickname


# 用来记录用户的登录记录
class UserLoginLog(models.Model):
    objects = models.manager

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Login_set')
    log = models.CharField(max_length=255)
    logTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "UserLoginLog"
        verbose_name='登录日志'
        verbose_name_plural = verbose_name


# 鸡汤
class Jitang(models.Model):
    objects = models.manager

    addtime = models.DateTimeField(auto_now_add=True)
    jitang = models.CharField(max_length=255)

    class Meta:
        db_table = "Jitang"
        verbose_name='心灵鸡汤'
        verbose_name_plural = verbose_name
