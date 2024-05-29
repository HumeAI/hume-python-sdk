"""API request and response models for EVI configurations."""

from typing import List, Optional

from pydantic import ConfigDict

from hume._common.utilities.model_utilities import BaseModel
from hume._voice.models.tools_models import ToolMeta


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


class LanguageModelConfig(BaseModel):
    """Language model configuration for EVI."""

    model_provider: str
    model_resource: str
    temperature: Optional[float] = None

    model_config = ConfigDict(protected_namespaces=())


class PostPromptRequest(BaseModel):
    """Post request model for creating a new EVI prompt."""

    name: str
    version_description: Optional[str]
    text: Optional[str]


class VoiceIdentityConfig(BaseModel):
    """Configuration for changing the voice of EVI."""

    provider: Optional[str] = None
    name: Optional[str] = None


class ConfigResponse(BaseModel):
    """Response model for an EVI configurations."""

    id: str
    version: int
    version_description: Optional[str]
    name: str
    created_on: int
    modified_on: int
    prompt: Optional[PromptResponse]
    voice: Optional[VoiceIdentityConfig]


class ConfigsResponse(BaseModel):
    """Response model for a page of EVI configurations."""

    page_number: int
    page_size: int
    configs_page: List[ConfigResponse]


class BuiltinToolConfig(BaseModel):
    """Configuration for a built-in EVI tool."""

    name: str
    tool_type: str
    fallback_content: Optional[str]


class PostConfigRequest(BaseModel):
    """Post request model for creating a new EVI configuration."""

    name: str
    version_description: Optional[str]
    prompt: PromptMeta
    voice: Optional[VoiceIdentityConfig]
    language_model: Optional[LanguageModelConfig]
    tools: Optional[List[ToolMeta]]


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
    # TODO: Add tool info
    prompt: Optional[str]
    voice: Optional[VoiceIdentityConfig]
