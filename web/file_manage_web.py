from typing import List

from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from core.file_group_manage_process import group_get
from core.file_manage_process import files_save, get_list
from utils.reponse import BaseResponse

file = APIRouter()


@file.post("/upload", tags=["文件管理"], summary="文件上传")
async def upload(files: List[UploadFile] = File(...), group_id: int = Form(...)) -> BaseResponse:
    # 根据文件组id获取文件组信息
    group_uuid = await group_get(group_id)
    file_infos = await files_save(files, group_uuid, group_id)
    return BaseResponse(
        code=200,
        msg="success",
        data=file_infos
    )


@file.get("/list/{group_id}", tags=["文件管理"], summary="文件列表")
async def list(id: int) -> BaseResponse:
    data = await get_list(id)
    return BaseResponse(
        code=200,
        msg="success",
        data=data
    )