from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from time import time
from typing import Callable
from settings import TORTOISE_ORM, origins


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_prcess_time_header(request: Request, call_next: Callable):
    start_time = time()
    # request.state  in state we can add whanever we want, for exaple user, like request.state.user = user
    respose = await call_next(request)
    process_time = time() - start_time
    respose.headers["X-Process-Time"] = str(process_time)
    return respose


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)
