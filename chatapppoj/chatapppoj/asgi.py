"""
ASGI config for chatapppoj project.
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapppoj.settings')

django.setup()  #  make sure Django apps are loaded before imports

from chatapp.routing import websocket_urlpatterns  # import AFTER setup

application = ProtocolTypeRouter({
    'http': get_asgi_application(),  #  call the function
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
