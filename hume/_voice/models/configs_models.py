from typing import List, Optional

from hume._common.utilities.model_utilities import BaseModel


class PromptResponse(BaseModel):
    id: str
    version_number: int
    version_description: Optional[str]
    name: str
    created_on: int
    modified_on: int
    text: Optional[str]


class PromptsResponse(BaseModel):
    page_number: int
    page_size: int
    prompts: List[PromptResponse]


class PromptMeta(BaseModel):
    id: str
    version: int


class PostPromptRequest(BaseModel):
    name: str
    version_description: Optional[str]
    text: Optional[str]


class ConfigResponse(BaseModel):
    id: str
    version_number: int
    version_description: Optional[str]
    name: str
    created_on: int
    modified_on: int
    prompt: Optional[PromptResponse]


class ConfigsResponse(BaseModel):
    page_number: int
    page_size: int
    configs: List[ConfigResponse]


class PostConfigRequest(BaseModel):
    name: str
    version_description: Optional[str]
    prompt: PromptMeta


class ConfigMeta(BaseModel):
    id: str
    version: int


class VoiceConfig(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_on: int
    modified_on: int
    prompt: Optional[str]
