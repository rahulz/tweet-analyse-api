# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

import web.routing
from web.consumers import AnalyseConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'http': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                url('home', AnalyseConsumer)
            )
        ),
    )
})
