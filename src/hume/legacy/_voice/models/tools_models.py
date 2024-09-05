"""API request and response models for EVI tools."""

from __future__ import annotations

from hume.legacy._common.utilities.model_utilities import BaseModel


class ToolResponse(BaseModel):
    """Response model for an EVI tools."""

    id: str
    tool_type: str
    version: int
    version_description: str | None
    name: str
    created_on: int
    modified_on: int
    fallback_content: str | None
    description: str | None
    parameters: str


class ToolsResponse(BaseModel):
    """Response model for a page of EVI tools."""

    page_number: int
    page_size: int
    tools_page: list[ToolResponse]


class ToolMeta(BaseModel):
    """Tool metadata."""

    id: str
    version: int


class PostToolRequest(BaseModel):
    """Post request model for creating a new EVI tool."""

    name: str
    version_description: str | None
    description: str | None
    parameters: str
    fallback_content: str | None


class VoiceTool(BaseModel):
    """EVI tool."""

    id: str
    name: str
    created_on: int
    modified_on: int
    parameters: str
    description: str | None
    fallback_content: str | None
