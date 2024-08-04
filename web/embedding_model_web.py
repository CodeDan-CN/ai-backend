from fastapi import APIRouter

from core.embedding_model_process import add_embedding_model_info, get_embedding_model_info, \
    delete_embedding_model_info, update_embedding_model_info
from models.request import EmbeddingModelParameterRequest
from utils.reponse import BaseResponse

e_model = APIRouter()


@e_model.post("/add", response_model=BaseResponse)
async def create_embedding_parameter(param: EmbeddingModelParameterRequest):
    """ 添加模型配置 """
    result = await add_embedding_model_info(param)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )


@e_model.get("/get{id}/", response_model=BaseResponse)
async def get_embedding_parameter(id: int):
    """ 根据id获取模型配置信息 """
    result = await get_embedding_model_info(id)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )


@e_model.put("/update/{param_id}/", response_model=BaseResponse)
async def update_embedding_parameter(id: int, model_update: EmbeddingModelParameterRequest):
    result = await update_embedding_model_info(id, model_update)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )


@e_model.delete("/delete/{id}/", response_model=BaseResponse)
async def delete_embedding_parameter(id: int):
    """ 根据id删除模型配置 """
    count = await delete_embedding_model_info(id)
    return BaseResponse(
        code=200,
        msg="success",
        data=count
    )
