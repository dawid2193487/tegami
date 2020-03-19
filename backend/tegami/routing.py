from channels.routing import URLRouter
from channels.http import AsgiHandler
from django.urls import path
from django.conf.urls import url
from boards.consumers import ThreadConsumer

application = URLRouter([
    path("ws/thread/<int:thread_id>/", ThreadConsumer),
    url(r"", AsgiHandler),
])
