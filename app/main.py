from dataclasses import asdict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from library.helpers import *
from common.config import conf
from database.conn import db
from routers import twoforms, randoms, accordion, api_randoms


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # init DB
    c = conf()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    app.include_router(randoms.router)
    app.include_router(api_randoms.router)
    app.include_router(twoforms.router)
    app.include_router(accordion.router)
    
    return app

app = create_app()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("AboutMe.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


# @app.get("/page/{page_name}", response_class=HTMLResponse)
# async def show_page(request: Request, page_name: str):
#     data = openfile(page_name+".md")
#     return templates.TemplateResponse("page.html", {"request": request, "data": data})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)