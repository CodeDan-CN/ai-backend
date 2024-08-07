from abc import ABC, abstractmethod
from typing import Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter


class AbstractDocumentSplitActuator(ABC):
    """ 切割方式的抽象类 """

    @abstractmethod
    async def invoke(self, document):
        pass


class DocumentSplitActuatorFactory:
    services: Dict[str, AbstractDocumentSplitActuator] = {}

    @staticmethod
    def get_document_split(policy: str) -> AbstractDocumentSplitActuator:
        if policy not in DocumentSplitActuatorFactory.services:
            split_actuator = globals()[policy]()
            DocumentSplitActuatorFactory.services[policy] = split_actuator
        return DocumentSplitActuatorFactory.services.get(policy)


class RecursiveCharacterDocumentSplitter(AbstractDocumentSplitActuator):
    """ 递归字符切割实现类 """

    def __init__(self) -> None:
        self.chunk_size = 500
        self.chunk_overlap = 100

    async def invoke(self, document):
        text_split = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", "。", ",", " ", ""]
        )
        text_split_documents = text_split.split_documents(document)
        return text_split_documents
