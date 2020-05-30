from django.urls import path

from .views import thought, classifyText

app_name = 'compayu'

urlpatterns = [
    path('thought/', thought, name="thought"),
    path('classify-text/', classifyText.as_view(), name='classify-text')
]
