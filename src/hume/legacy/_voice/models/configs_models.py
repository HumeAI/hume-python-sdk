"""API request and response models for EVI configurations."""

from __future__ import annotations

from pydantic import ConfigDict

from hume.legacy._common.utilities.model_utilities import BaseModel
from hume.legacy._voice.models.tools_models import ToolMeta


class PromptResponse(BaseModel):
    """Response model for an EVI prompt."""

    id: str
    version: int
    version_description: str | None
    name: str
    created_on: int
    modified_on: int
    text: str | None


class PromptsResponse(BaseModel):
    """Response model for a page of EVI prompts."""

    page_number: int
    page_size: int
    prompts: list[PromptResponse]


class PromptMeta(BaseModel):
    """Prompt metadata."""

    id: str
    version: int


class LanguageModelConfig(BaseModel):
    """Language model configuration for EVI."""

    model_provider: str
    model_resource: str
    temperature: float | None = None

    model_config = ConfigDict(protected_namespaces=())


class PostPromptRequest(BaseModel):
    """Post request model for creating a new EVI prompt."""

    name: str
    version_description: str | None
    text: str | None


class VoiceIdentityConfig(BaseModel):
    """Configuration for changing the voice of EVI."""

    provider: str
    name: str | None = None


class ConfigResponse(BaseModel):
    """Response model for an EVI configurations."""

    id: str
    version: int
    version_description: str | None
    name: str
    created_on: int
    modified_on: int
    prompt: PromptResponse | None
    voice: VoiceIdentityConfig | None


class ConfigsResponse(BaseModel):
    """Response model for a page of EVI configurations."""

    page_number: int
    page_size: int
    configs_page: list[ConfigResponse]


class BuiltinToolConfig(BaseModel):
    """Configuration for a built-in EVI tool."""

    name: str
    tool_type: str
    fallback_content: str | None


class PostConfigRequest(BaseModel):
    """Post request model for creating a new EVI configuration."""

    name: str
    version_description: str | None
    prompt: PromptMeta
    voice: VoiceIdentityConfig | None
    language_model: LanguageModelConfig | None
    tools: list[ToolMeta] | None


class ConfigMeta(BaseModel):
    """EVI configuration metadata."""

    id: str | None
    version: int | None


class VoiceConfig(BaseModel):
    """EVI configuration."""

    id: str
    name: str
    description: str | None
    created_on: int
    modified_on: int
    prompt: str | None
    voice: VoiceIdentityConfig | None
