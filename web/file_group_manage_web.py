from fastapi import APIRouter

from core.file_group_manage_process import group_add, group_list, group_delete, group_update
from utils.reponse import BaseResponse

group = APIRouter()


@group.post("/add", tags=["文件组管理"], summary="进行文件组的添加")
async def add(group_name: str):
    data = await group_add(group_name)
    return BaseResponse(
        code=200,
        mesaage="success",
        data=data
    )

@group.get("/list", tags=["文件组管理"], summary="进行文件组的添查看")
async def list():
    data = await group_list()
    return BaseResponse(
        code=200,
        mesaage="success",
        data=data
    )

@group.put("/update", tags=["文件组管理"], summary="进行文件组修改")
async def update(id:int,new_name:str):
    await group_update(id,new_name)
    return BaseResponse(
        code=200,
        mesaage="success"
    )

@group.delete("/delete/{id}", tags=["文件组管理"], summary="进行文件组删除")
async def delete(id:int):
    await group_delete(id)
    return BaseResponse(
        code=200,
        mesaage="success"
    )