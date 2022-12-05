from os import path
import sys
import time

from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
app_dir = path.join(base_dir, 'app')

# abspath
sys.path.append(path.abspath(app_dir))
from api.get_randoms import Random, get_random
from exceptions.types import isInt_nonegative, isNatural

from dotenv import load_dotenv
load_dotenv()
rands = Random()

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/api/random")

@router.get("/", response_class=HTMLResponse)
def init(request: Request):

    rands.__init__()
    print("\n\nInitialized\n\n")
    context = {
        "request": request
    }
    html = "api_randoms.html"
    return templates.TemplateResponse(html, context=context)

@router.post("/result", response_class=HTMLResponse)
def post_random(request: Request, integer: str = Form(...) or None):
    
    integer = integer.strip()
    
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
    
    html = "api_randoms.html"
    return templates.TemplateResponse(html, context)

@router.post("/add", response_class=HTMLResponse)
def post_randoms(request: Request, integers: str = Form(...)):
    
    integers = integers.strip()
    
    error_1 = False
    error_msg_1 = "0 이상의 정수를 입력해 주세요."
    if isInt_nonegative(integers):
        integers = int(integers)
        if integers not in rands.integers:
            rands.integers.append(integers)
    else:
        if integers != "":
            error_1 = True
    
    context = {
        "request": request,
        "integers": rands.integers,
        "error_1": error_1,
        "error_msg_1": error_msg_1,
    }
    
    html = "api_randoms.html"
    return templates.TemplateResponse(html, context)

@router.post("/iterations", response_class=HTMLResponse)
async def post_iterations(request: Request, iterations: str = Form(...)):
    
    rands.init_df()
    iterations = iterations.strip()
    
    randoms: bool = False
    error_2: bool = False
    error_msg_2 = "1 이상의 정수를 입력해 주세요."
    error_msg_3 = "1개 이상의 수를 입력해 주세요."
    if isNatural(iterations):
        rands.preprocessed(int(iterations))
        randoms = rands.save_df_to_png()
        plots = rands.save_plot_to_png()
    else:
        plots: bool = False
        randoms: bool = False
        if iterations != "":
            error_2 = True
    
    context = {
        "request": request,
        "integers": rands.integers,
        "error_2": error_2,
        "error_msg_2": error_msg_2,
        "error_msg_3": error_msg_3,
        "randoms": randoms,
        "plots": plots,
    }

    html = "api_randoms.html"
    return templates.TemplateResponse(html, context)