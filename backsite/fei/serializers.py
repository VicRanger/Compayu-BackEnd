from rest_framework import serializers
from compayu.models import Thought, Media, Editor

class ThoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thought
        fields = "__all__" #将整个表的所有字段都序列化

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = "__all__" #将整个表的所有字段都序列化