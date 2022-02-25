from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.base import BaseHTTPMiddleware

from middlewares import add_prcess_time_header
from settings import TORTOISE_ORM_DEV, TORTOISE_ORM_TEST, origins
from routers import users_router, items_router


def build_app(env):
    app = FastAPI()
    app.include_router(users_router)
    app.include_router(items_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=add_prcess_time_header)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    if env == "dev":
        register_tortoise(app, config=TORTOISE_ORM_DEV, add_exception_handlers=True)
    elif env == "test":
        register_tortoise(app, config=TORTOISE_ORM_TEST, add_exception_handlers=True)
    else:
        NotImplemented("this env is not supported yet")
    return app


app = build_app("dev")
test_app = build_app("test")
