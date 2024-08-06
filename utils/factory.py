class EmbeddingModelFactory():
    """ 嵌入模型工厂 """
    model_server: dict = {}

    @classmethod
    def init_model(cls, model: str):
        """ 根据嵌入模型名称获取嵌入模型实例获取方法 """
        if model not in cls.model_server:
            # 通过反射的方式进行对应模型的创建
            split_actuator = globals()[model]()
            cls.model_server[model] = split_actuator
        return cls.model_server.get(model)
