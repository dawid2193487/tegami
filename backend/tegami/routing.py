from channels.routing import URLRouter
from channels.http import AsgiHandler
from django.urls import path
from django.conf.urls import url
from boards.consumers import AccessConsumer

from channels.auth import AuthMiddlewareStack

application = AuthMiddlewareStack(URLRouter([
    path("ws/", AccessConsumer),
    url(r"", AsgiHandler),
]))
