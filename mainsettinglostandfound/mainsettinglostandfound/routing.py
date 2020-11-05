from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#Changed
import lostandfoundweb.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(#Changed
            lostandfoundweb.routing.websocket_urlpatterns
        )
    ),
})