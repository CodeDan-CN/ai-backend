from fastapi import APIRouter
from core.template_manage_process import add_model_template, update_model_template_info
from core.template_manage_process import get_model_template_info
from models.request import ModelTemplateRequest
from utils.reponse import BaseResponse

template = APIRouter()


@template.post("/templates/add", response_model=BaseResponse)
async def create_model_template(template: ModelTemplateRequest):
    """ 添加模型模版 """
    result = await add_model_template(template.type, template.name, template.alias)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )


@template.get("/templates/{template_id}/", response_model=BaseResponse)
async def get_model_template(template_id: int):
    """ 根据id获取模版的信息 """
    result = await get_model_template_info(template_id)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )


@template.put("/templates/{template_id}/", response_model=BaseResponse)
async def update_model_template(template_id: int, template: ModelTemplateRequest):
    result = await update_model_template_info(template_id, template.name, template.type, template.alias)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )


@template.delete("/model_templates/{template_id}/")
async def delete_model_template(template_id: int):
    delete_count = await delete_model_template(template_id)
    return BaseResponse(
        code=200,
        msg="success",
        data=delete_count
    )

