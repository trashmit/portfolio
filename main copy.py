from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles 
import asyncio
import time
import asyncio
import users
import portfolio
import management

app = FastAPI()

app.include_router(users.router)
app.include_router(portfolio.router)
app.include_router(management.router)

app.mount(
    "/app", 
    StaticFiles(directory = "app"),
    name = "app"
)

templates = Jinja2Templates(directory="app")


@app.get("/")
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/portfolio/")
async def portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})

@app.get("/keys/")
async def keys(request: Request):
    return templates.TemplateResponse("keys.html", {"request": request})

@app.get("/chart/")
async def keys(request: Request):
    return templates.TemplateResponse("c.html", {"request": request})
