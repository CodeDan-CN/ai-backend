# Milvus连接配置
MILVUS_DB_CONFIG = {
    "host": "localhost",
    "port": "19530",
    "username": "",
    "password": "",
    "db_name": "default",
}

# TORTOISE连接pgsql配置
TORTOISE_ORM_PGSQL = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            'credentials': {
                'database': 'odoo',
                'host': '10.3.74.219',  # david的本地地址
                'password': 'root',
                'port': '5432',
                'user': 'root',
            }
        }
    },
    'apps': {
        'models': {
            "models": ["models.pgsql_model"]
        }
    },
    'timezone': 'Asia/Shanghai'
}

# 临时文件存储路径
FILE_CONFIG = {
    "path": "/Users/codedan/local/project/pycharmProjects/digital_portrait/file/"
}

# 日志文件配置
LOG_CONFIG = {
    "url" : "/Users/codedan/local/project/pycharmProjects/ai-backend-cn/log",
    "name": "ai-backend-cn",
    "time_format": "%Y-%m-%d"  # 修改时间格式以包含分钟
}



