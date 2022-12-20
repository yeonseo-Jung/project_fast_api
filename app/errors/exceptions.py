'''
from app.errors import exceptions as ex

from app.errors.exceptions import APIException, SqlFailureEx, APIQueryStringEx

'''

import sys
from os import path
# abspath
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.common.consts import MAX_API_KEY, MAX_API_WHITELIST

class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405

class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception
    
    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "000000",
        msg: str = None,
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)
        
    
class SqlFailureEx(APIException):
    def __init__(self, ip: str, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"{ip}는 올바른 IP가 아닙니다.",
            detail=f"invalid IP: {ip}",
            code=f"{StatusCode.HTTP_400}{'6'.zfill(4)}",
            ex=ex,
        )
    
class APIQueryStringEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"쿼리스트링은 key, timestamp 2개만 허용되며, 2개 모두 요청시 제출되어야 합니다.",
            detail="Query String Only Accept key and timestamp.",
            code=f"{StatusCode.HTTP_400}{'7'.zfill(4)}",
            ex=ex,
        )

class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"로그인이 필요한 서비스 입니다.",
            detail="Authorization Required",
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            ex=ex,
        )
        
class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"세션이 만료되어 로그아웃 되었습니다.",
            detail="Token Expired",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )
        
class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"비정상적인 접근입니다.",
            detail="Token has been compromised.",
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            ex=ex,
        )