"""API request and response models for EVI tools."""

from typing import List, Optional

from hume._common.utilities.model_utilities import BaseModel


class ToolResponse(BaseModel):
    """Response model for an EVI tools."""

    id: str
    tool_type: str
    version: int
    version_description: Optional[str]
    name: str
    created_on: int
    modified_on: int
    fallback_content: Optional[str]
    description: Optional[str]
    parameters: Optional[str]




class ToolsResponse(BaseModel):
    """Response model for a page of EVI tools."""

    page_number: int
    page_size: int
    tools_page: List[ToolResponse]


class VoiceIdentityTool(BaseModel):
    """Tool for changing the voice of EVI."""

    provider: Optional[str] = None
    name: Optional[str] = None


class PostToolRequest(BaseModel):
    """Post request model for creating a new EVI tool."""

    name: str
    version_description: Optional[str]
    voice: VoiceIdentityTool


class ToolMeta(BaseModel):
    """EVI tool metadata."""

    id: Optional[str]
    version: Optional[int]


class VoiceTool(BaseModel):
    """EVI tool."""

    id: str
    name: str
    description: Optional[str]
    created_on: int
    modified_on: int
    prompt: Optional[str]
