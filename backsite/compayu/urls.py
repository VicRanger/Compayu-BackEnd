from django.urls import path

from .views import thought, classifyText,login

app_name = 'compayu'

urlpatterns = [
    path('thought/', thought.as_view(), name="thought"),
    path('login/', login.as_view(), name="login"),
    path('classify-text/', classifyText.as_view(), name='classify-text')
]
