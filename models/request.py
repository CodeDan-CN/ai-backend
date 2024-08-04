from typing import Optional

from pydantic import BaseModel


class ModelTemplateRequest(BaseModel):
    type: int
    name: str
    alias: Optional[str] = None


class ModelTemplateResponse(BaseModel):
    id: int
    type: int
    name: str
    alias: Optional[str]

    class Config:
        orm_mode = True


class EmbeddingModelParameterRequest(BaseModel):
    model_template_id: int
    model_key: str
    model_url: str
    user_id: str


class EmbeddingModelParameterResponse(BaseModel):
    id: int
    model_template_id: int
    model_key: str
    model_url: str

    class Config:
        orm_mode = True
