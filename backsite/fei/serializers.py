from rest_framework import serializers
from compayu.models import UserProfile, Thought, Media

class ThoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thought
        fields = "__all__" #将整个表的所有字段都序列化