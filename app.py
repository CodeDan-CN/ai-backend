import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config.setting import TORTOISE_ORM_PGSQL
from exception.all_exception import global_exception_handlers
from utils.logger_factory import logger
from tortoise.contrib.fastapi import register_tortoise


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
    # _app.include_router(router=embedding, prefix="/v1/embedding", tags=["embedding"])

    # pgsql_db_config = TORTOISE_ORM_PGSQL['connections']['default']['credentials']

    # 注册PostgreSQL数据源
    # register_tortoise(
    #     _app,
    #     db_url=f"asyncpg://{pgsql_db_config['user']}:{pgsql_db_config['password']}@{pgsql_db_config['host']}:{pgsql_db_config['port']}/{pgsql_db_config['database']}",
    #     modules={'models': ['models.pgsql_model']},
    #     # generate_schemas=True,
    #     add_exception_handlers=True,
    # )

    return _app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host=os.environ.get('SERVER_HOST', '0.0.0.0'), port=int(os.environ.get('SERVER_PORT', 8001)))
