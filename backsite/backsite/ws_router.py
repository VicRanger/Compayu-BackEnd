from channels.routing import ProtocolTypeRouter, URLRouter
import compayu.ws_urls
from django.urls import path
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket':
    URLRouter(
        compayu.ws_urls.websocket_urlpatterns
    ),
})
