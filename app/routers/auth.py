import sys
from os import path
from datetime import datetime, timedelta

import bcrypt
import jwt
from dataclasses import asdict
from fastapi import APIRouter, Depends

# TODO:
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# abspath
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.common.consts import Jwt
from app.database.models import Users
from app.database.schemas import SnsType, Token, UserToken, UserRegister
from app.common.config import conf
from app.database.conn import db

c = conf()
conf_dict = asdict(c)
db.init_db(**conf_dict)
_jwt = Jwt()

router = APIRouter(prefix="/auth")


@router.post("/register/{sns_tyoe}", status_code=201, response_model=Token)
async def register(sns_type: SnsType, reg_info: UserRegister, session: Session = Depends(db.session)):
    """_summary_

    Args:
        sns_type (SnsType): _description_
        reg_info (UserRegister): _description_
        session (Session, optional): _description_. Defaults to Depends(db.session).
    """
    if sns_type == SnsType.email:
        if not reg_info.email or not reg_info.pw:
            return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided"))
        
        # check eamil 
        is_exist = await is_email_exist(reg_info.email)
        if is_exist:
            return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))
        
        # hashing pw
        hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
        new_user = Users.create(session, auto_commit=True, pw=hash_pw, email=reg_info.email)
        
        # create access token
        token = dict(
            Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw', 'marketing_agree'}),)}"
        )
        return token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


@router.post("/login/{sns_type}", status_code=200, response_model=Token)
async def login(sns_type: SnsType, user_info: UserRegister):
    if sns_type == SnsType.email:
        if not user_info.email or not user_info.pw:
            return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided"))
        
        # check email
        is_exist = await is_email_exist(user_info.email)
        if not is_exist:
            return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        
        # check pw
        user = Users.get(email=user_info.email)
        is_verified = bcrypt.checkpw(user_info.pw.encode("utf-8"), user.pw.encode("utf-8"))
        if not is_verified:
            return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))

        # create access token
        token = dict(
            Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'pw', 'marketing_agree'}),)}"
        )
        return token
    
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))

        
async def is_email_exist(email: str):
    get_email = Users.get(email=email)
    if get_email:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, _jwt.JWT_SECRET, algorithm=_jwt.JWT_ALGORITHM)
    return encoded_jwt