from modules.items.handlers import router as items_router
from modules.users.handlers import router as users_router
from modules.pages.handlers import router as page_router
from modules.graph_ql.handlers import graphql_app as graph_ql_router
from modules.events.handlers import router as events_router
from modules.web_socket.handlers import router as web_socket_router
from modules.callbacs.handlers import router as call_backcs_router

__all__ = (
    items_router,
    users_router,
    page_router,
    graph_ql_router,
    events_router,
    web_socket_router,
    call_backcs_router
)
