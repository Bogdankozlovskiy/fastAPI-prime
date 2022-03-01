from fastapi import Request, Response
from typing import Callable
from time import time


async def add_prcess_time_header(request: Request, call_next: Callable) -> Response:
    start_time = time()
    # request.state  in state we can add whanever we want, for exaple user, like request.state.user = user
    respose = await call_next(request)
    process_time = time() - start_time
    respose.headers["X-Process-Time"] = str(process_time)
    return respose
