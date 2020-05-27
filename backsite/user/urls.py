# coding = utf-8
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # BASEDIR/user/
    path('', views.userPage),

    # BASEDIR/user/usercenter
    path("usercenter/", views.userCenter),

    # BASEDIR/user/login
    url(r'login/$', views.LoginView.as_view()),

    # BASEDIR/user/register/?with=???
    path("register/", views.checkRegister),

    # BASEDIR/user/register/sendemail
    path("register/sendemail", views.initEmail),

    # BASEDIR/user/register/sendvalidcode
    path("register/sendvalidcode", views.initPhone),
]

