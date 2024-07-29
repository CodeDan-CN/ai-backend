from typing import List
from uuid import uuid4

from exception.custom_exception import CustomErrorThrowException
from models.model import FileGroup


async def group_add(group_name: str) -> str:
    """ 新增文件组 """
    file_group = await FileGroup.filter(group_name=group_name).first()
    if file_group:
        raise CustomErrorThrowException(100010, "文件组名称重复,请换一个名字")
    uuid = uuid4().hex
    file_group = await FileGroup.create(**{"group_name": group_name, "group_uuid": uuid})
    return file_group.group_name


async def group_get(group_id: int) -> str:
    """ 根据id获取文件组uuid """
    if not group_id:
        raise CustomErrorThrowException(100014, "文件组id不存在，请检查文件组状态")
    group_info = await FileGroup.filter(id=group_id).first()
    return group_info.group_uuid


async def group_list():
    """ 查询全部文件组 """
    file_groups = await FileGroup.all()
    group_names = [{"group_name": file_group.group_name} for file_group in file_groups]
    return group_names


async def group_update(id: int, new_group_name: str):
    file_group = await FileGroup.filter(group_name=new_group_name).first()
    if file_group:
        raise CustomErrorThrowException(100010, "文件组名称重复,请换一个名字")
    old_file_group = await FileGroup.filter(id=id).first()
    if not old_file_group:
        raise CustomErrorThrowException(100011, "文件组不存在,请检查id")
    await FileGroup.filter(id=id).update(**{"group_name": new_group_name})


async def group_delete(id: int) -> None:
    """ 删除指定文件组 """
    await FileGroup.filter(id=id).delete()
