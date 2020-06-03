from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
import random

from backsite.settings import LOGIN_TIME
from backsite.token import getUserByToken
from compayu.models import Thought, Editor
from fei.serializers import ThoughtSerializer
from user.models import User, UserInfo, Jitang, Avatar


def setting(request):
    response = {}
    what = request.POST.get("what", '')
    if what == '':
        response['msg'] = '未获取参数'
        return JsonResponse(response)
    if what == 'logintime':
        response['data'] = LOGIN_TIME
        response['msg'] = '登录保存时间'
    return JsonResponse(response)


def getuserinfo(request):
    response = {'msg': '用户数据API', 'code': '200'}
    what = request.POST.get("what", '')
    # print(what)
    if what == '':
        response['msg'] = '未获取参数'
        return JsonResponse(response)
    else:
        token = request.POST.get('token')
        uid = getUserByToken(token)
        if what == 'avatar':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                user = User.objects.filter(id=uid)[0]
                response['msg'] = '用户头像链接'
                response['data'] = str(user.avatar)
                response['code'] = '200'
            return JsonResponse(response)
        elif what == 'nickname':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                user = User.objects.filter(id=uid)[0]
                response['msg'] = '用户昵称'
                response['data'] = str(user.nickname)
                response['code'] = '200'
            return JsonResponse(response)
        elif what == 'thoughtContent':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                tid = request.POST.get('id', '')
                tcontent = Editor.objects.filter(id=tid)
                if tcontent.count() > 0:
                    response['msg'] = '想法编辑器实例'
                    response['content'] = tcontent[0].content
                    response['text'] = tcontent[0].text
                    response['code'] = '200'
                else:
                    response['msg'] = '未查询到数据'
                    response['code'] = '404'
        elif what == 'userinfo':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                user = User.objects.filter(id=uid)[0]
                userinfo = UserInfo.objects.filter(user=user)[0]
                # user
                response["nickname"] = user.nickname
                response["phonenum"] = user.phonenum
                response["email"] = user.email
                response["signup_type"] = user.signup_type
                response["usertype"] = user.userType
                response["level"] = user.level
                # userinfo
                response["signature"] = userinfo.signature
                response["gender"] = userinfo.gender
                response["birthday"] = userinfo.birthday
            return JsonResponse(response)
        elif what == 'jitang':
            jitang = Jitang.objects.filter()
            rand = random.randint(1, jitang.count())
            response['data'] = jitang[rand-1].jitang
            response['code'] = '200'
            response['msg'] = '获得心灵鸡汤'
        elif what == 'setuser':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                where = request.POST.get('where', '')
                if where != '':
                    # print(where)
                    user = User.objects.filter(id=uid)[0]
                    userinfo = UserInfo.objects.filter(user=user)[0]
                    if where == 'signature':
                        data = request.POST.get('data', '')
                        userinfo.signature = data
                    if where == 'genderAndBirthday':
                        gender = request.POST.get('gender')
                        birth = request.POST.get('birth')
                        userinfo.gender = gender
                        userinfo.birthday = birth
                    userinfo.save()
                    user.save()
                    response['msg'] = '用户数据更新: '+where
                    response['code'] = '200'
            return JsonResponse(response, safe=False)
        elif what == 'thought':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                where = request.POST.get('where', '')
                if where == 'mostView':
                    mythought = Thought.objects.filter(author_id=uid, isdelete=False).order_by('-views')
                    # 只取前两个
                    count = mythought.count()
                    if count >= 2:
                        count = 2
                    response['num'] = count
                    response['data'] = ThoughtSerializer(mythought, many=True).data
                    response['code'] = '200'
                    response['msg'] = '最多人阅读Thought'
                elif where == 'newest':
                    mythought = Thought.objects.filter(author_id=uid, isdelete=False).order_by('-create_time')
                    # 只取前两个
                    count = mythought.count()
                    if count >= 2:
                        count = 2
                    response['num'] = count
                    response['data'] = ThoughtSerializer(mythought, many=True).data
                    response['code'] = '200'
                    response['msg'] = '最新Thought'
                elif where == 'all' or where == '':
                    mythought = Thought.objects.filter(author_id=uid, isdelete=False)
                    count = mythought.count()
                    response['num'] = count
                    response['data'] = ThoughtSerializer(mythought, many=True).data
                    response['code'] = '200'
                    response['msg'] = '所有Thought'
                elif where == 'filter':
                    myfilter = request.POST.get('filter', '')
                    page = request.POST.get('page', '')
                    # filter : time , view , search
                    if myfilter == 'time':
                        mythought = Thought.objects.filter(author_id=uid, isdelete=False).order_by('-create_time')
                        paginator = Paginator(mythought, 10)
                        if page == '':
                            thispage = paginator.page(1)
                        else:
                            thispage = paginator.page(int(page))
                        count = mythought.count()
                        response['num'] = count
                        response['data'] = ThoughtSerializer(thispage, many=True).data
                        response['code'] = '200'
                        response['msg'] = '最新Thought'
                    elif myfilter == 'view':
                        mythought = Thought.objects.filter(author_id=uid, isdelete=False).order_by('-views')
                        paginator = Paginator(mythought, 10)
                        if page == '':
                            thispage = paginator.page(1)
                        else:
                            thispage = paginator.page(int(page))
                        count = mythought.count()
                        response['num'] = count
                        response['data'] = ThoughtSerializer(thispage, many=True).data
                        response['code'] = '200'
                        response['msg'] = '最多浏览Thought'
                    elif myfilter == 'search':
                        search = request.POST.get('search', '')
                        isDate = False
                        for i in search:
                            if i == '-':
                                isDate = True
                        if isDate:
                            date = search.split('-')
                            mythought = Thought.objects.filter(author_id=uid, isdelete=False, create_time__year=date[0], create_time__month=date[1], create_time__day=date[2]).order_by('-create_time')
                            if mythought.count() == 0:
                                # 减少要求
                                mythought = Thought.objects.filter(author_id=uid, isdelete=False,
                                                                        create_time__month=date[1],
                                                                        create_time__day=date[2]).order_by('-create_time')
                        else:
                            mythought = Thought.objects.filter(author_id=uid, isdelete=False, title=search).order_by('-create_time')
                        paginator = Paginator(mythought, 10)
                        if page == '':
                            thispage = paginator.page(1)
                        else:
                            thispage = paginator.page(int(page))
                        count = mythought.count()
                        response['num'] = count
                        response['data'] = ThoughtSerializer(thispage, many=True).data
                        response['code'] = '200'
                        response['msg'] = '搜索结果Thought'
        elif what == 'thoughtcount':
            if uid == 0:
                response['msg'] = '未查询到数据'
                response['code'] = '404'
            elif uid == -1:
                response['msg'] = '您的token已过期，请重新登录'
                response['code'] = '403'
            else:
                mythought = Thought.objects.filter(author_id = uid)
                tnum = mythought.count()
                response['tnum'] = tnum
                tview = 0
                for i in range(0,tnum):
                    tview = tview + int(mythought[i].views)
                response['vnum'] = tview
                response['msg'] = '想法量计数'
                response['code'] = '200'
    return JsonResponse(response)


# 检查token是否有效，是否过期
def checktoken(request):
    response = {'msg': 'token有效性API', 'code': '200'}
    token = request.POST.get('token', '')
    if token != '':
        uid = getUserByToken(token)
        if uid != 0 and uid != -1:
            response['data'] = 'True'
        else:
            response['data'] = 'False'
    return JsonResponse(response)


# 更新用户头像路径
def changeAvatar(request):
    response = {'msg': '未获取到数据', 'code': '400'}
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        token = request.POST.get('token')
        uid = getUserByToken(token)
        if uid == 0:
            response['msg'] = '未查询到数据'
            response['code'] = '404'
        elif uid == -1:
            response['msg'] = '您的token已过期，请重新登录'
            response['code'] = '403'
        else:
            user = User.objects.filter(id=uid)[0]
            date = str(timezone.now().date()).replace('-', '')
            qiniu = Avatar.objects.filter(user=user)
            link = 'https://cdn.wzz.ink/'+'avatar/'+date+'/'+avatar.name
            link = link.replace('=', '')
            link = link.replace('&', '')
            link = link.replace(',', '')
            if qiniu.count() != 0:
                # 如果有就更新
                qiniu = qiniu[0]
                qiniu.link = link
                qiniu.picture = avatar
                qiniu.save()
            else:
                # 如果没有就重新创建
                qiniu = Avatar(user=user, picture=avatar, link=link)
                qiniu.save()
            user.avatar = link
            user.save()
            print(link)
            response['msg'] = '用户头像已更新'
            response['data'] = str(user.avatar)
            response['code'] = '200'

    return JsonResponse(response)