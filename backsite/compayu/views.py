from django.shortcuts import render
from compayu.models import Thought
# Create your views here.
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
from django.core import serializers
import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context
import time
import os
from compayu.util import writeThought


@csrf_exempt
def thought(req):
    ret = {}
    if req.method == 'GET':
        query_data = req.GET.dict()
        thought_list = []
        if 'type' in query_data:
            thoughts = Thought.objects.filter(
                type_raw=query_data['type']).order_by('-create_time')
            if thoughts.count() <= 0:
                return HttpResponse(json.dumps({'data': []}, ensure_ascii=False))
            tail = 1
            if 'number' in query_data:
                tail = min(int(query_data['number']), thoughts.count())
            thoughts = thoughts[:tail]
            for item in thoughts:
                obj = item.json()
                thought_list.append(obj)
            ret['data'] = thought_list
        else:
            ret['data'] = '您的输入无法识别'
        res = HttpResponse(json.dumps(ret, ensure_ascii=False))
        return res
    if req.method == 'POST':
        query_data = json.loads(req.body.decode('UTF-8'))
        print(query_data)
        obj = writeThought(query_data)
        obj.save()
        ret['data'] = obj.json()
        print(ret)
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
    ret['data'] = 'NONE'
    return HttpResponse(json.dumps(ret, ensure_ascii=False))
