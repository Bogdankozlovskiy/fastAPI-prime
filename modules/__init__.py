from modules.items.controllers import router as items_router
from modules.users.controllers import router as users_router
from modules.pages.controllers import router as page_router
from modules.graph_ql.controllers import graphql_app as graph_ql_router
from modules.events.controllers import router as events_router
from modules.web_socket.controllers import router as web_socket_router
from modules.callbacs.controllers import router as call_backcs_router

__all__ = (
    items_router,
    users_router,
    page_router,
    graph_ql_router,
    events_router,
    web_socket_router,
    call_backcs_router
)
