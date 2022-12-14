# from pydantic import BaseModel

# class StocksBase(BaseModel):
#     stock_code: str
#     stock_name: str
#     market: str
#     close: float
#     open: float
#     high: float
#     low: float
#     volume: float
#     amounts: float
#     market_cap: float
#     shares: float

# class Stocks(StocksBase):
#     id: int
    
#     class Config:
#         orm_mode = True
        
        
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr, IPvAnyAddress


class UserRegister(BaseModel):
    # pip install 'pydantic[email]'
    email: str = None
    pw: str = None


class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"


class Token(BaseModel):
    Authorization: str = None


class EmailRecipients(BaseModel):
    name: str
    email: str


class SendEmail(BaseModel):
    email_to: List[EmailRecipients] = None


class KakaoMsgBody(BaseModel):
    msg: str = None


class MessageOk(BaseModel):
    message: str = Field(default="OK")


class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True


class AddApiKey(BaseModel):
    user_memo: str = None

    class Config:
        orm_mode = True


class GetApiKeyList(AddApiKey):
    id: int = None
    access_key: str = None
    created_at: datetime = None


class GetApiKeys(GetApiKeyList):
    secret_key: str = None


class CreateAPIWhiteLists(BaseModel):
    ip_addr: str = None


class GetAPIWhiteLists(CreateAPIWhiteLists):
    id: int

    class Config:
        orm_mode = True
    