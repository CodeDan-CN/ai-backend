from abc import ABC

from langchain_openai import OpenAIEmbeddings


class AbstractEmbeddingModel(ABC):
    """ 抽象模型初始化类 """

    async def init_embedding_model(self, texts, model_name: str, model_key: int, model_base_url: str = None):
        pass


class OpenAIEmbeddingModel(AbstractEmbeddingModel):
    """ openAI的嵌入模型初始化类 """
    async def init_embedding_model(self, texts, model_name: str, model_key: int, model_base_url: str = None):
        # 进行模型的初始化，并使用此模型进行操作
        return OpenAIEmbeddings(model=model_name, api_key=model_key, openai_api_base=model_base_url,
                                dimensions=1024)
