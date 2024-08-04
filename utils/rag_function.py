from langchain_openai import OpenAIEmbeddings


class RagUnifiedOperation:

    @classmethod
    async def get_embedding_model(cls, texts, model_name: str, model_key: int, model_base_url: str = None):
        # 进行模型的初始化，并使用此模型进行操作
        embeddings_model = OpenAIEmbeddings(model=model_name, api_key=model_key, openai_api_base=model_base_url,
                                            dimensions=1024)
        return
