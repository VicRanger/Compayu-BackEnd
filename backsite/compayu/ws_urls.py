from django.urls import re_path

from compayu.consumers import ThoughtComsumer

websocket_urlpatterns = [
    re_path('thought/', ThoughtComsumer),
]
