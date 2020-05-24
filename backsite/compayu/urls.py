from django.urls import path

from . import views

app_name = 'compayu'

urlpatterns = [
    path('thought/', views.thought, name="thought"),
]
