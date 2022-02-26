from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=['pages'])


@router.get("/page", response_class=HTMLResponse)
async def get_page(request: Request, page_id: Optional[int] = Query(None)):
    return templates.TemplateResponse("index.html", {"request": request, "id": page_id})
