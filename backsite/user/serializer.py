# 序列化数据
from rest_framework import serializers
from . import models


# 用户信息序列化
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
