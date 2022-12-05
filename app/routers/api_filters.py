import sys
from os import path
from dataclasses import asdict

import pandas as pd

from sqlalchemy import Column, func
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.orm import Session

from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# abspath
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.common.constants import Quarters
# from app.database.crud import get_filter
# from app.database.models import Stocks, Amounts, Ratios
from app.database.models import Accounts
from app.api.filters import Filter


filter = Filter()
accounts = filter.dart_amounts.account_nm_eng.unique()
ratios = filter.dart_ratios.ratio.unique()
quarters = Quarters()
templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/api/filter")


@router.get("/", response_class=HTMLResponse)
def init(request: Request):
    
    # init filter
    filter.init_filter()
    print("\n\nInitialized\n\n")
    filter.quarters = list(quarters.quarters.values())[:8]
    # quarters_key = quarters.quarters.keys()
    context = {
        "request": request,
        # "quarters": quarters_key,
        "accounts": accounts,
        "ratios": ratios,
    }
    html = "api_filters.html"
    return templates.TemplateResponse(html, context=context)

# @router.post("/result", response_class=HTMLResponse)
# def post_filter(request: Request, quarter: str = Form(...) or None):
    
#     # print("\n\n", quarter, type(quarter), "\n\n")
#     request_dict = request.__dict__
#     _form = request_dict["_form"]
#     print("\n\n", _form, "\n\n")
    
#     for key, val in _form.items():
#         print(key, val)
#     # print("\n\n", _form.keys(), "\n\n")
#     print("\n\n", _form["quarter"], "\n\n")
#     context = {
#         "request": request
#     }
#     html = "api_filters.html"
#     return templates.TemplateResponse(html, context=context)

@router.post("/add_amount", response_class=HTMLResponse)
def post_add(request: Request, account: str = Form(...) or None, min_amount: str = Form(...) or None, max_amount: str = Form(...) or None):
    
    min_amount, max_amount, status = filter.preprocessor(min_amount, max_amount, "amount")
    if status:
        filter.amounts[account] = [min_amount, max_amount]
    
    context = {
        "request": request,
        "accounts": accounts,
        "ratios": ratios,
        "_amounts": filter.amounts,
        "_ratios" :filter.ratios,
    }
    html = "api_filters.html"
    return templates.TemplateResponse(html, context=context)

@router.post("/add_ratio", response_class=HTMLResponse)
def post_add(request: Request, ratio: str = Form(...) or None, min_ratio: str = Form(...) or None, max_ratio: str = Form(...) or None):
    
    min_ratio, max_ratio, status = filter.preprocessor(min_ratio, max_ratio, "ratio")
    if status:
        filter.ratios[ratio] = [min_ratio, max_ratio]
    
    context = {
        "request": request,
        "accounts": accounts,
        "ratios": ratios,
        "_amounts": filter.amounts,
        "_ratios" :filter.ratios,
    }
    html = "api_filters.html"
    return templates.TemplateResponse(html, context=context)

@router.post("/result", response_class=HTMLResponse)
def post_result(request: Request):
    # filtering & intersecting
    filter.filter_amounts()
    filter.filter_ratios()
    filter.intersect()
    
    context = {
        "request": request,
        "accounts": accounts,
        "ratios": ratios,
        "_amounts": filter.amounts,
        "_ratios" :filter.ratios,
    }
    html = "api_filters.html"
    return templates.TemplateResponse(html, context=context)