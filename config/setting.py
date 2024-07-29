# Milvus连接配置
MILVUS_DB_CONFIG = {
    "host": "localhost",
    "port": "19530",
    "username": "",
    "password": "",
    "db_name": "default",
}

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            'credentials': {
                "host": "127.0.0.1",
                'port': '3306',
                'user': 'root',
                'password': 'Zld19981016..',
                'database': 'ai-backend',
                'echo': True
            }
        }
    },
    'apps': {
        'models': {
            "models": ["models.model"]
        }
    },
    'timezone': 'Asia/Shanghai'
}


# 临时文件存储路径
FILE_CONFIG = {
    "path": "/Users/codedan/local/project/pycharmProjects/ai-backend-cn/file/"
}

# 日志文件配置
LOG_CONFIG = {
    "url" : "/Users/codedan/local/project/pycharmProjects/ai-backend-cn/log",
    "name": "ai-backend-cn",
    "time_format": "%Y-%m-%d"  # 修改时间格式以包含分钟
}



