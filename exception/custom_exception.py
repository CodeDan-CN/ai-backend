from fastapi import HTTPException


class BaseAPIException(HTTPException):
    status_code = 400
    detail = "api error"

    def __init__(self, detail: str = None, status_code: int = None):
        self.detail = detail or self.detail
        self.status_code = status_code or self.status_code


class CustomErrorThrowException(BaseAPIException):
    """ 自定义异常 """
    status_code = 999
    detail = None

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=detail)
