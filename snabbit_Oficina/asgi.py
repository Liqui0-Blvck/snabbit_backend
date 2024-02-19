"""
ASGI config for snabbit_Oficina project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# 

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snabbit_Oficina.settings')

# application = get_asgi_application()

import os
from channels.routing import ProtocolTypeRouter
# from channels.auth import 
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snabbit_Oficina.settings')
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
  'http': django_asgi_app,
  
})