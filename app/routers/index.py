from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

index_router = APIRouter()
@index_router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@index_router.get("/health", status_code=200)
async def health():
    return {"status": "ok"}
