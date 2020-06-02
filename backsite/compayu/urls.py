from django.urls import path

from .views.thought import thought, classifyText, thought_view
from .views.login import login,logout
from .views.init import init
from .views.user import user
app_name = 'compayu'

urlpatterns = [
    path('thought/', thought.as_view(), name="thought"),
    path('thought-view/', thought_view.as_view(), name="thought-view"),
    path('login/', login.as_view(), name="login"),
    path('logout/', logout.as_view(), name="logout"),
    path('user/', user.as_view(), name="user"),
    path('init/', init.as_view(), name="init"),
    path('classify-text/', classifyText.as_view(), name='classify-text')
]
