from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .serializers import ThoughtSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile, Thought, Media
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django import forms
import time

@csrf_exempt


# Create your views here.

class ThoughtAPIView(APIView):
    def get(self, request, format=None):
        thought_id = self.request.query_params.get("id", 0)
        thoughts = Thought.objects.filter(thought_id = int(thought_id))
        thoughts_serializer = ThoughtSerializer(thoughts, many=True)
        return Response(thoughts_serializer.data)

def upload(request):
    return render(request, "index.html")

# def postImg(request):

#     Media.objects.create(
#         picture = request.data["file"]
#     )

#     return Response({
#         "success": False,
#         "msg": "新增图片",
#         "results": ""
#     }, )

# def uploadImg(request):
#     date = time.strftime("%Y%m%d",time.localtime(time.time()))
#     if request.method == 'POST':
#         new_img = Media(
#             picture = request.FILES.get('img'),
#             link = 'q9ekh65im.bkt.clouddn.com/' + 'pictures/' + date + '/' + request.FILES.get('img').name
#         )
#         new_img.save()
#     return render(request, 'upload.html')

class postImg(APIView):
    def post(self,request):
        res={}
        date = time.strftime("%Y%m%d",time.localtime(time.time()))
        # print(request.FILES)
        # print(request.FILES.get('file'))
        new_img = Media(
            picture = request.FILES.get('file'),
            link = 'https://cdn.wzz.ink/' + 'pictures/' + date + '/' + request.FILES.get('file').name
        )
        new_img.save()

        res['code']=200
        res['message']='上传成功'
        res['link'] = 'https://cdn.wzz.ink/' + 'pictures/' + date + '/' + request.FILES.get('file').name

        return JsonResponse(res)