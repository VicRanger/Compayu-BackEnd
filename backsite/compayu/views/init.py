
from compayu.models import Thought, Editor
from user.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

class init(APIView):
    def get(self, request, format=None):
        if User.objects.all().count() <= 0:
            newuser = User(password='123456', nickname='管理员', email='test@q.q',
                           signup_type='email', lastlogin=timezone.now(), signup_time=timezone.now())
            newuser.save()
            data = [
                {'text': '第一条开心', 'type_raw': "happy"},
                {'text': '第一条生气', 'type_raw': "angry"},
                {'text': '第一条讨厌', 'type_raw': "disgust"},
                {'text': '第一条悲伤', 'type_raw': "sad"},
            ]
            for d in data:
                editor = Editor(content=d['text'], text=d['text'])
                editor.save()
                t = Thought(type_raw=d['type_raw'], rich_text=editor)
                t.save()
            return Response('init')
        return Response('already init')
