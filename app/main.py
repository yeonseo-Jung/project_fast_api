from dataclasses import asdict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from library.helpers import *
from common.config import conf
from database.conn import db
from database.models import Base
from app.middlewares.token_validator import access_control
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from routers import twoforms, accordion, api_randoms, api_filters, auth, index


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # init DB
    c = conf()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    
    # create tables    
    # Base.metadata.create_all(bind=db._engine)
    
    # middlewares
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])
    
    # routers
    app.include_router(index.router)
    
    app.include_router(auth.router)
    
    app.include_router(api_randoms.router)
    app.include_router(api_filters.router)
    
    app.include_router(twoforms.router)
    app.include_router(accordion.router)
    
    return app

app = create_app()
templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)