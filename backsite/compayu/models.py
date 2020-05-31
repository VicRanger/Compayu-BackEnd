from django.db import models
from django.utils import timezone
import datetime
# from django.contrib.auth.models import AbstractUser
from wangeditor.fields import WangRichTextField
from user.models import User



'''
Designed by Fei 
'''

class Editor(models.Model):
    content = WangRichTextField()
    text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Editor'  # 自己设计表名
        verbose_name = '富文本'
        verbose_name_plural = verbose_name


'''
Designed by Fei 
'''

class Media(models.Model):
    link = models.CharField(max_length=255, blank=True, null=True)
    media_type = models.CharField(max_length=20, blank=True, null=True)
    picture = models.ImageField(blank=True,
                                null=True,
                                upload_to="pictures/%Y%m%d",
                                max_length=255,
                                verbose_name="图片")

    class Meta:
        db_table = 'Media'  # 自己设计表名
        verbose_name = '媒体存储'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.link, self.media_type)


'''
Designed by Fei 
'''


# class UserProfile(AbstractUser):
#     nickname = models.CharField(max_length=255, blank=True, null=True)
#     phonenum = models.CharField(max_length=11)
#     validcode = models.CharField(max_length=255, blank=True, null=True)
#     wxopenid = models.CharField(max_length=255, blank=True, null=True)
#     signup_type = models.CharField(max_length=255, blank=True, null=True)
#     is_signup = models.IntegerField(default=0)
#     signup_time = models.DateTimeField(blank=True, null=True)
#     signature = models.CharField(max_length=255, blank=True, null=True)

#     # 以下为暴力删除
#     # first_name = None
#     # last_name = None #已经有nickname了
#     # 好吧，删了这些就无法创建超级管理员了
#     # groups = None #分组
#     # user_permissions = None #权限。一个用户可以拥有多个权限，一个权限可以被多个用户所有用。和Permission属于一种多对多的关系。
#     # is_staff = None #是否可以进入到admin的站点。代表是否是员工。
#     # is_active = None #是否是可用的。对于一些想要删除账号的数据，我们设置这个值为0就可以了，而不是真正的从数据库中删除。
#     # is_superuser = None #是否是超级管理员。如果是超级管理员，那么拥有整个网站的所有权限。

#     class Meta:
#         db_table = 'UserProfile'
#         verbose_name = '用户'
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         # return '%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.username, self.password, self.nickname, self.phonenum, self.validcode, self.email, self.wxopenid, self.signup_type, self.is_signup, self.last_login, self.signup_time, self.date_joined, self.signature)
#         return self.username


'''
Designed by Fei 
Modified by wzz 0525
'''


class Thought(models.Model):
    title = models.CharField(max_length=40)
    text = models.TextField()
    type_raw = models.CharField(max_length=20)
    type_ai = models.CharField(max_length=20, blank=True, null=True)
    type_human = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(default=timezone.now)
    modified_time = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(
        User, related_name='thought_author', blank=True, null=True, on_delete=models.CASCADE)
    picture = models.ForeignKey(
        Media, related_name='thought_media', on_delete=models.SET_NULL, blank=True, null=True)
    rich_text = models.ForeignKey(
        Editor, related_name='thought_content', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'Thought'
        verbose_name = '想法'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_raw + ' - ' + self.text[:10] + ' : ' + str(self.modified_time)

    def json(self):
        ret = {}
        fields = ['id','title','text','type_raw','create_time','views']
        for f in fields:
            ret[f] = str(getattr(self, f))
        return ret