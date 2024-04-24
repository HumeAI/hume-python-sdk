"""API request and response models for EVI configurations."""

from typing import List, Optional

from hume._common.utilities.model_utilities import BaseModel


class PromptResponse(BaseModel):
    """Response model for an EVI prompt."""

    id: str
    version: int
    version_description: Optional[str]
    name: str
    created_on: int
    modified_on: int
    text: Optional[str]


class PromptsResponse(BaseModel):
    """Response model for a page of EVI prompts."""

    page_number: int
    page_size: int
    prompts: List[PromptResponse]


class PromptMeta(BaseModel):
    """Prompt metadata."""

    id: str
    version: int


class PostPromptRequest(BaseModel):
    """Post request model for creating a new EVI prompt."""

    name: str
    version_description: Optional[str]
    text: Optional[str]


class ConfigResponse(BaseModel):
    """Response model for an EVI configurations."""

    id: str
    version: int
    version_description: Optional[str]
    name: str
    created_on: int
    modified_on: int
    prompt: Optional[PromptResponse]


class ConfigsResponse(BaseModel):
    """Response model for a page of EVI configurations."""

    page_number: int
    page_size: int
    configs_page: List[ConfigResponse]


class VoiceIdentityConfig(BaseModel):
    """Configuration for changing the voice of EVI."""

    provider: Optional[str] = None
    name: Optional[str] = None


class PostConfigRequest(BaseModel):
    """Post request model for creating a new EVI configuration."""

    name: str
    version_description: Optional[str]
    prompt: PromptMeta
    voice: VoiceIdentityConfig


class ConfigMeta(BaseModel):
    """EVI configuration metadata."""

    id: Optional[str]
    version: Optional[int]


class VoiceConfig(BaseModel):
    """EVI configuration."""

    id: str
    name: str
    description: Optional[str]
    created_on: int
    modified_on: int
    prompt: Optional[str]
