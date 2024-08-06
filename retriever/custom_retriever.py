from langchain_milvus import Milvus
from typing import List
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class MilvusRetriever(BaseRetriever):
    embeddings = None
    """ 嵌入模型 """
    connection_args: dict
    """ milvus连接配置 """
    collection_name: str
    """ 集合名称 """
    k: int
    """Number of top results to return"""
    search_kwargs: dict
    """这是标量检索字段"""

    def do_similarity_search(self, query: str, search_kwargs: dict, k=10):
        """ 根据问题进行相似度检索，返回相似度高的数据 """
        expr = f"file_label == '{label}'"
        milvus_store = Milvus(
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
            connection_args=self.connection_args
        )
        result = milvus_store.similarity_search(query=query, k=k, expr=expr)
        return result

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """ 通过自定义检索获取相似片段 """
        return self.do_similarity_search(query, k=self.k, search_kwargs=self.search_kwargs)
