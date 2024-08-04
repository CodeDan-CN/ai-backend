from tortoise.transactions import in_transaction

from exception.custom_exception import CustomErrorThrowException
from models.model import EmbeddingModelParameter
from models.request import EmbeddingModelParameterRequest
from utils.logger_factory import logger


async def add_embedding_model_info(param: EmbeddingModelParameterRequest):
    """ 添加模型配置 """
    model = await EmbeddingModelParameter.filter(model_template_id=param.model_template_id, model_key=param.model_key,
                                                 model_url=param.model_url, user_id=param.user_id)
    if model:
        logger.error("该模型配置已存在，请再次检查操作")
        raise CustomErrorThrowException("该模型配置已存在，请再次检查操作")
    new_model = await EmbeddingModelParameter.create(**param.dict())
    return new_model


async def get_embedding_model_info(id: int):
    """ 根据id获取模型配置信息 """
    embedding = await EmbeddingModelParameter.filter(id=id).first()
    if not embedding:
        logger.error("该模型配置不存在，请再次检查操作")
        raise CustomErrorThrowException("该模型配置不存在，请再次检查操作")
    return embedding


async def update_embedding_model_info(id, model_update: EmbeddingModelParameterRequest):
    """ 根据id更新模型配置 """
    async with in_transaction():
        param = await EmbeddingModelParameter.filter(id=id).first()
        if param is None:
            raise CustomErrorThrowException("EmbeddingModelParameter not found")
        await param.update_from_dict(model_update.dict(exclude_unset=True))
        await param.save()
    return param


async def delete_embedding_model_info(id: int):
    """ 根据id删除模型配置 """
    count = await EmbeddingModelParameter.filter(id=id).delete()
    return count
