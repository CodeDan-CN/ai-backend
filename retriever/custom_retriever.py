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
        # 如果 search_kwargs 不为空，则生成 expr
        if search_kwargs:
            # 将 search_kwargs 中的键值对转换为 Milvus 的 expr 表达式
            conditions = []
            for key, value in search_kwargs.items():
                if isinstance(value, str):
                    conditions.append(f"{key} == '{value}'")
                elif isinstance(value, (int, float)):
                    conditions.append(f"{key} == {value}")
                elif isinstance(value, list):
                    # 如果值是列表，可以生成一个 IN 表达式
                    value_list = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in value)
                    conditions.append(f"{key} IN ({value_list})")
                # 你可以根据需要扩展更多类型的处理逻辑
            expr = " AND ".join(conditions)
        else:
            expr = ""
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
