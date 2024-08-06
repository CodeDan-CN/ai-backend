from models.model import ModelTemplate
from utils.logger import logger


async def add_model_template(model_type: int, model_name: str, model_alias: str):
    """ 添加模型模版 """
    # 检测这个模型模版是否存在
    template = await ModelTemplate.filter(type=model_type, name=model_name).first()
    if template:
        logger.error("该模版也存在，请再次检查操作")
    new_template = await ModelTemplate.create(type=model_type, name=model_alias, alias=model_alias)
    return new_template


async def get_model_template_info(id: int):
    """ 根据id获取模版的信息 """
    template = await ModelTemplate.filter(id=id).first()
    if not template:
        logger.error("该模版不存在，请再次检查操作")
    return template


async def update_model_template_info(id: int, name: str, type: int, alias: str):
    """ 修改模型模版 """
    template = await get_model_template_info(id)
    # 修改改变的部分
    await template.update_from_dict(**{"id": id, "name": name, "type": type, "alias": alias})
    # 保存实体
    await template.save()
    return template


async def delete_model_template(id: int):
    """ 根据id删除模型模版 """
    deleted_count = await ModelTemplate.filter(id=id).delete()
    return deleted_count
