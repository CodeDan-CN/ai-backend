import os.path
import shutil
from typing import List
from fastapi import UploadFile
from config.setting import FILE_CONFIG
from exception.custom_exception import CustomErrorThrowException
from models.model import FileRecord
from utils.logger import logger

base_file_url = FILE_CONFIG["path"]


async def files_save(files: List[UploadFile], group_uuid: str, group_id: int) -> List:
    """ 将文件存储到对应的文件路径下 """
    if not files:
        return []
    # 根据基础文件路径拼接uuid得到目前文件组的服务器存储路径
    directory_path = base_file_url + "/" + group_uuid
    # 如果路径不存在，则创建
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Directory :'{directory_path}' created.")
    file_infos = []
    file_record = []
    try:
        # 开始迭代进行文件的写入,并进行文件路径的临时存储
        for file in files:
            name = file.filename
            input_file_url = f"{directory_path}/{name}"
            # 接受文件并写入
            with open(input_file_url, "wb") as f:
                for line in file.file:
                    f.write(line)
            file_infos.append({"file_name": name, "file_url": input_file_url})
            file_extension = name.split('.')[-1]
            file_record.append(FileRecord(file_name=name, file_type=file_extension, group_id=group_id))
    except Exception as e:
        logger.error(f"文件上传失败，原因是:{str(e)}")
        # 整个文件夹的删除，检查文件夹是否存在
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            # 删除整个文件夹及其所有内容
            shutil.rmtree(directory_path)
        raise CustomErrorThrowException(f"文件上传失败，原因是:{str(e)}")
    # 文件记录的插入
    await FileRecord.bulk_create(file_record)
    return file_infos


async def get_list(group_id):
    """ 根据文件组id获取当前文件组下所属文件 """
    file_infos = await FileRecord.filter(group_id=group_id).all()
    return [{"file_name": file_info.file_name, "file_type": file_info.file_type} for file_info in file_infos]
