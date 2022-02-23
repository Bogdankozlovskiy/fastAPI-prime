from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from time import time
from typing import Callable


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


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
    respose = await call_next(request)
    process_time = time() - start_time
    respose.headers["X-Process-Time"] = str(process_time)
    return respose


register_tortoise(
    app,
    db_url="postgres://peewee_user:1234@localhost:5432/peewee_db",
    modules={"models": ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
