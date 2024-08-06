import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.setting import TORTOISE_ORM
from exception.all_exception import global_exception_handlers
from utils.logger import logger
from tortoise.contrib.fastapi import register_tortoise

from web.file_group_manage_web import group
from web.file_manage_web import file


def create_app():
    _app = FastAPI(
        title="ai-backend-cn",
        version="v1.0.0",
        # 全局以及自定义异常捕获
        exception_handlers=global_exception_handlers
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @_app.on_event("startup")
    async def app_startup():
        # 使用间隔触发器添加任务
        # scheduler.add_job(my_task, IntervalTrigger(seconds=10), id='my_task_id')
        logger.info("fastAPI ------------------ Starting")


    @_app.on_event("shutdown")
    async def shutdown_event():
        logger.info("fastAPI ------------------ ending")

    # 添加路由
    _app.include_router(router=group, prefix="/v1/group", tags=["group"])
    _app.include_router(router=file, prefix="/v1/file", tags=["file"])

    # 配置数据库
    register_tortoise(
        app=_app,
        config=TORTOISE_ORM,
        # generate_schemas =True, 没有表自动生成，生产不开
        add_exception_handlers=True  # 数据库日志，同样生产不开
    )

    return _app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host=os.environ.get('SERVER_HOST', '0.0.0.0'), port=int(os.environ.get('SERVER_PORT', 8000)))
