from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .serializers import ThoughtSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from compayu.models import UserProfile, Thought, Media
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django import forms
import time




# Create your views here.
@csrf_exempt
class ThoughtAPIView(APIView):
    def get(self, request, format=None):
        thought_id = self.request.query_params.get("id", 0)
        thoughts = Thought.objects.filter(thought_id = int(thought_id))
        thoughts_serializer = ThoughtSerializer(thoughts, many=True)
        return Response(thoughts_serializer.data)

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