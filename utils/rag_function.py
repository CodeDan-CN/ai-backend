from abc import ABC

from langchain_milvus import Milvus

from config.setting import MILVUS_DB_CONFIG
from retriever.custom_retriever import MilvusRetriever


class RagUnifiedOperation(ABC):
    """ RAG操作类 """

    async def from_document(self, docs):
        """ 进行向量化并存库 """
        pass

    async def similarity_search(self, query: str):
        """ 检索出向量 """
        pass


class RagMilvusVector(RagUnifiedOperation):
    """ Milvus RAG操作类 """
    embeddings = None
    vector_store = None
    vector_store_config = None
    collection_name = None
    k = None
    search_kwargs = None

    def __init__(self, collection_name: str, embeddings):
        milvus_db = MILVUS_DB_CONFIG
        self.connection_args = {
            "host": milvus_db['host'],
            "port": milvus_db['port'],
            "username": milvus_db['username'],
            "password": milvus_db['password'],
            "db_name": milvus_db['db_name']
        }
        self.vector_store = Milvus
        self.collection_name = collection_name,
        self.embeddings = embeddings

    def get_custom_retriever(self):
        """ 初始化检索器 """
        return MilvusRetriever(embeddings=self.embeddings, connection_args=self.connection_args,
                               collection_name=self.collection_name, k=self.k, search_kwargs=self.search_kwargs)

    async def from_document(self, docs):
        """ 进行向量化并存库 """
        vector_db = self.vector_store.from_documents(documents=docs, embedding=self.embeddings,
                                                     connection_args=self.vector_store_config)
        return vector_db
