from typing import List
from langchain_community.document_loaders import TextLoader
from core.embedding_model_process import get_embedding_model_info
from core.template_manage_process import get_model_template_info
from utils.document_spilt_actuator import DocumentSplitActuatorFactory
from utils.factory import EmbeddingModelFactory
from utils.logger import logger
from utils.rag_function import RagMilvusVector


async def text_split_by_file_infos(file_infos: List[dict], policy: str):
    """ 根据指定策略进行文件的切分，并返回切分片段 """
    load_documents = []
    # 首先进行文件的加载
    for file_info in file_infos:
        url = file_info["url"]
        name = file_info["name"]
        loader = TextLoader(url)
        documents = loader.load()
        # 将文件元数据放入对应document中
        await add_document_metadata(name=name, documents=documents)
        load_documents.extend(documents)
    # 进行全部内容的切割(使用切割器工厂)
    text_split = DocumentSplitActuatorFactory.get_document_split(policy=policy)
    split_documents = await text_split.invoke(load_documents)
    return split_documents


async def show_text_split_document(split_documents):
    """ 展示切分结果，进行数据脱敏

        splite_documents:[
            Document(metadata:{"file_name":value},page_content:"document1"),
            Document(metadata:{"file_name":value},page_content:"document2"),
            ......
        ]

        数据格式：
        [
            {
               "file_name":value,
               "file_documents":[
                    "document_1",
                    "document_2",
               ]
            },
            ......
        ]

    """
    result = {}
    for document in split_documents:
        file_name = document.metadata.get("file_name", "unknown")  # 获取文件名，默认为 "unknown"
        page_content = document.page_content.strip()  # 获取文档内容，并去除两边空白

        if file_name not in result:
            result[file_name] = {"file_name": file_name, "file_documents": []}

        result[file_name]["file_documents"].append(page_content)

        # 将字典转换为列表，以符合返回格式
    return list(result.values())


async def add_document_metadata(name: str, documents):
    """ 添加document的元数据 """
    for document in documents:
        document.metadata["file_name"] = name


async def embedding(file_infos: List[dict], policy: str, model_id: int):
    """ 进行嵌入 """
    documents = await text_split_by_file_infos(file_infos, policy)
    # 检查模型配置是否存在
    embeddings_info = await get_embedding_model_info(model_id)
    if not embeddings_info:
        logger.error("模型配置不存在，请重新确认！")
    template = await get_model_template_info(embeddings_info.model_template_id)
    # 如果存在，则进行模型获取过程
    embedding_model = EmbeddingModelFactory.init_model(template.name)
    # 将模型交给langchain进行向量数据库写入
    milvus = RagMilvusVector("ai_backend", embedding_model)
    milvus.from_document(documents)


async def retriever_invoke(question: str, top_k: int, search_kwargs):
    """ 根据问题和表达式进行混合检索 """
    milvus = RagMilvusVector("ai_backend", None)
    retriever = milvus.get_custom_retriever(top_k, search_kwargs)
    retriever.invoke(question)
