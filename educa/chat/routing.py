from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    # if using the django channels 3.x, the below code has to be changed: 
    # https://channels.readthedocs.io/en/stable/releases/3.0.0.html#update-to-asgi-3
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
