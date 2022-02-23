from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time
from typing import Callable
from settings import origins


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
    respose = await call_next(request)
    process_time = time() - start_time
    respose.headers["X-Process-Time"] = str(process_time)
    return respose
