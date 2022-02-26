from fastapi import APIRouter


router = APIRouter()


@router.on_event("startup")
async def on_start():
    print("start application")


@router.on_event("shutdown")
async def on_shuting():
    print("shuting down application")
