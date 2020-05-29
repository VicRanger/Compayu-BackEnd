"""backsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.conf.urls.static import static
from . import settings
from fei.views import postImg #fei
from . import views

urlpatterns = [
    path('compayu/',include('compayu.urls')),
    path('admin/', admin.site.urls),
    path('upload/', postImg, name='imageUpload'), #七牛云图片上传-fei
    # by Lin
    path('user/', include('user.urls')),  # BASEDIR/user/ 用户管理系统
    path('', views.indexPage),  # BASEDIR 门户页面
    path('website/', include('website.urls')),  # BASEDIR/website/ 网站数据页面，备案号啊，关于我们什么的
    path('api/', include('api.urls')),  # BASEDIR/api/ 各种接口
]
urlpatterns += static('static-url/', document_root=settings.STATIC_ROOT)