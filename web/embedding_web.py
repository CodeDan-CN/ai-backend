from typing import List

from fastapi import APIRouter

from core.embedding_process import text_split_by_file_infos, show_text_split_document
from utils.reponse import BaseResponse

embedding = APIRouter()


@embedding.post("/textSplit", tags=["嵌入管理"], summary="将文件加载后按照用户要求进行嵌入")
async def text_split(file_info: List[dict], policy: str):
    split_documents = await text_split_by_file_infos(file_infos=file_info, policy=policy)
    result = await show_text_split_document(split_documents)
    return BaseResponse(
        code=200,
        msg="success",
        data=result
    )
