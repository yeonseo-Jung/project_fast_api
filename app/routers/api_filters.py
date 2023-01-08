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
from app.common.consts import Quarters
from app.database.crud import get_filter
from app.database.models import Accounts, Stocks, Amounts, Ratios
from app.api.filters import Filter

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/api/filter")

filter = Filter()
accounts = filter.dart_amounts.account_nm_eng.unique()
ratios = filter.dart_ratios.ratio.unique()
quarters = Quarters()


@router.get("/", response_class=HTMLResponse)
def init(request: Request):
    
    # init filter
    filter.init_filter()
    
    # 최근 8분기 
    filter.quarters = list(quarters.quarters.values())[:8]
    
    context = {
        "request": request,
        "accounts": accounts,
        "ratios": ratios,
    }
    html = "api_filters.html"
    return templates.TemplateResponse(html, context=context)


@router.post("/add_amount", response_class=HTMLResponse)
def post_add_amount(request: Request, account: str = Form(...) or None, min_amount: str = Form(...) or None, max_amount: str = Form(...) or None):
    
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
def post_add_ratio(request: Request, ratio: str = Form(...) or None, min_ratio: str = Form(...) or None, max_ratio: str = Form(...) or None):
    
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
    codes_filtered = filter.codes_filtered
    
    context = {
        "request": request,
        "accounts": accounts,
        "ratios": ratios,
        "_amounts": filter.amounts,
        "_ratios": filter.ratios,
        "codes": codes_filtered,
    }
    html = "api_filters.html"
    return templates.TemplateResponse(html, context=context)