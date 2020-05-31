# coding = utf-8

from django.urls import path
from . import views

urlpatterns = [
    # BASEDIR/website/
    path('', views.websitePage),

]