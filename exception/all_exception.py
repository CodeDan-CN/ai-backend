from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from exception.custom_exception import BaseAPIException
from utils.logger import logger

exception = FastAPI()


# 定义全局变量捕获
async def global_exception_handler(request: Request, exc: Exception):
    # 打印异常信息
    logger.error(f"发生未处理的异常: {str(exc)}", exc_info=True)

    # 检查异常是否具有 'status_code' 属性
    status_code = getattr(exc, 'status_code', 999)

    if status_code == 500:
        message = getattr(exc, 'args', str(exc))
        err_msg = message[0] if message else 'Internal Server Error'
    else:
        # 尝试获取异常的 'detail' 属性，如果没有则使用异常的字符串表示
        err_msg = getattr(exc, 'detail', str(exc))

    if not status_code and not err_msg:
        status_code = 999,
        err_msg = str(exc)


    # 返回 JSON 响应
    return JSONResponse(
        {
            'code': status_code,
            'message': err_msg,
        }
    )


# 定义自定义异常捕获
async def variable_exception_handler(request, exc: BaseAPIException):
    code = exc.status_code
    message = exc.detail
    logger.error(f"发生未处理的异常: {str(exc)}", exc_info=True)
    return JSONResponse({
        'code': code,
        'message': message
    })


# 整理两种异常处理
global_exception_handlers = {
    BaseAPIException: variable_exception_handler,
    Exception: global_exception_handler
}
