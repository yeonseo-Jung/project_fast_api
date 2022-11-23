import os
import sys
import time

from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# root(app) 절대경로 추가
sys.path.append(os.path.abspath(BASE_DIR))
from api.get_randoms import Random, get_random
from exceptions.types import isInt_nonegative, isNatural

from dotenv import load_dotenv
load_dotenv()
rands = Random()

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/random", response_class=HTMLResponse)
def randoms(request: Request):
    # key = os.getenv("random_key")
    # print(key)
    rands.init_ints()
    print("\n\n", rands.integers, "\n\n")
    html = "random.html"
    context = {
        "request": request
    }
    return templates.TemplateResponse(html, context=context)

@router.post("/random/result", response_class=HTMLResponse)
def post_random(request: Request, integer: str = Form(...) or None):
    
    integer = integer.strip()
    
    html = "random.html"
    error = False
    error_msg = "0 이상의 정수를 입력해 주세요."
    if isInt_nonegative(integer):
        init = time.time()
        rand_n = get_random(int(integer))
        elapsed_ms = round((time.time() - init) * 1000, 3)
    else:
        integer, rand_n, elapsed_ms = None, None, None
        if integer != "":
            error = True
        
    context = {
        "request": request,
        "integer": integer,
        "random_number": rand_n,
        "elapsed_ms": elapsed_ms,
        "error_0": error,
        "error_msg": error_msg,
    }
    
    return templates.TemplateResponse(html, context)

@router.post("/random/add", response_class=HTMLResponse)
def post_randoms(request: Request, integers: str = Form(...)):
    
    integers = integers.strip()
    
    html = "random.html"
    error_1 = False
    error_msg_1 = "0 이상의 정수를 입력해 주세요."
    if isInt_nonegative(integers):
        rands.integers.append(int(integers))
    else:
        if integers != "":
            error_1 = True
    
    context = {
        "request": request,
        "integers": rands.integers,
        "error_1": error_1,
        "error_msg_1": error_msg_1,
    }
    
    return templates.TemplateResponse(html, context)

@router.post("/random/iterations", response_class=HTMLResponse)
async def post_iterations(request: Request, iterations: str = Form(...)):
    
    iterations = iterations.strip()
    
    html = "random.html"
    error_2 = False
    error_msg_2 = "1 이상의 정수를 입력해 주세요."
    if isNatural(iterations):
        rands.save_df_to_png(int(iterations))
        randoms = True
    else:
        randoms = False
        if iterations != "":
            error_2 = True
    
    context = {
        "request": request,
        "integers": rands.integers,
        "error_2": error_2,
        "error_msg_2": error_msg_2,
        "randoms": randoms,
    }
    
    return templates.TemplateResponse(html, context)