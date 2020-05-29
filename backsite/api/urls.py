# coding = utf-8
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # BASEDIR/api/settings/?what = ???
    path('settings/', views.setting),

    # BASEDIR/api/user/?what = ???
    path('user/', views.getuserinfo),

    # BASEDIR/api/token
    path('token/', views.checktoken),

    # BASEDIR/api/avatar
    path('avatar/', views.changeAvatar),
]