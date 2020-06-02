from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .serializers import ThoughtSerializer, ContentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from compayu.models import  Thought, Media, Editor
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django import forms
import time
import json, re #fei




# Create your views here.
# @csrf_exempt
# class ThoughtAPIView(APIView):
#     def get(self, request, format=None):
#         thought_id = self.request.query_params.get("id", 0)
#         thoughts = Thought.objects.filter(thought_id = int(thought_id))
#         thoughts_serializer = ThoughtSerializer(thoughts, many=True)
#         return Response(thoughts_serializer.data)

class postImg(APIView):
    def post(self,request):
        res={}
        date = time.strftime("%Y%m%d",time.localtime(time.time()))
        # print(request.FILES.keys())
        # print(request.FILES)

        new_img = Media(
            picture = request.FILES.get('file'),
            link = 'https://cdn.wzz.ink/' + 'pictures/' + date + '/' + request.FILES.get('file').name
        )
        new_img.save()


        # 给富文本
        res['message']='上传成功'
        res['errno'] = 0
        res['data'] = ['https://cdn.wzz.ink/' + 'pictures/' + date + '/' + request.FILES.get('file').name]

        return JsonResponse(res)

class Content(APIView):
    def get(self, request, format=None):
        content_id = self.request.query_params.get("id", 0)
        contents = Editor.objects.filter(id = int(content_id))
        contents_serializer = ContentSerializer(contents, many=True)
        return Response(contents_serializer.data)

@csrf_exempt
def editor(request):
    data = json.loads(request.body)
    front_content = data.get("content")
    front_text = data.get("text")
    front_text = front_text.replace(r"&nbsp;", "")
    front_text = filter_emoji(front_text)
    editor_content = Editor(
        content = front_content,
        text = front_text
    )
    editor_content.save()
    return JsonResponse({"result": True})

def filter_emoji(desstr,restr=''):  
    #过滤 emoji，本质是去掉所有四字节 utf8   
    try:  
        co = re.compile(u'[\U00010000-\U0010ffff]')  
    except re.error:  
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')  
    return co.sub(restr, desstr)  