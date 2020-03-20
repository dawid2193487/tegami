from channels.routing import URLRouter
from channels.http import AsgiHandler
from django.urls import path
from django.conf.urls import url
from boards.consumers import AccessConsumer

application = URLRouter([
    path("ws/", AccessConsumer),
    url(r"", AsgiHandler),
])
