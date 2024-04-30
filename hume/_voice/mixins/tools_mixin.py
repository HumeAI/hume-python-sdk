"""Client operations for managing EVI tools."""

import logging
from typing import Iterator, Optional

from hume._common.client_base import ClientBase
from hume._common.utilities.paging_utilities import Paging
from hume._voice.models.tools_models import PostToolRequest, ToolResponse, ToolsResponse, VoiceTool
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


# pylint: disable=redefined-builtin
class ToolsMixin(ClientBase):
    """Client operations for managing EVI tools."""

    def create_tool(
        self,
        *,
        name: str,
        parameters: str,
        fallback_content: Optional[str] = None,
        description: Optional[str] = None,
    ) -> VoiceTool:
        """Create a new EVI tool.

        Args:
            name (str): Tool name.
            parameters (str): Stringified JSON defining the parameters used by the tool.
            fallback_content (Optional[str]): Text to use if the tool fails to generate content.
            description (Optional[str]): Tool description.
        """
        post_tool_request = PostToolRequest(
            name=name,
            description=description,
            version_description=None,
            parameters=parameters,
            fallback_content=fallback_content,
        )
        post_tool_body = post_tool_request.to_json_str()
        endpoint = self._build_endpoint("evi", "tools")
        response = self._request(endpoint, method="POST", body_json_str=post_tool_body)
        tool_response = ToolResponse.model_validate_json(response.text)

        return self._tool_from_response(tool_response)

    def get_tool(self, id: str, _version: Optional[int] = None) -> VoiceTool:
        """Get an EVI tool by its ID.

        Args:
            id (str): Tool ID.
        """
        route = f"tools/{id}" if _version is None else f"tools/{id}/version/{_version}"
        endpoint = self._build_endpoint("evi", route)
        response = self._request(endpoint, method="GET")
        tools_response = ToolsResponse.model_validate_json(response.text)
        if len(tools_response.tools_page) == 0:
            raise HumeClientException(f"Tool not found with ID: {id}")

        return self._tool_from_response(tools_response.tools_page[0])

    def _iter_tool_versions(self, id: str) -> Iterator[VoiceTool]:
        endpoint = self._build_endpoint("evi", f"tools/{id}")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            tools_response = ToolsResponse.model_validate_json(response.text)
            if len(tools_response.tools_page) == 0:
                break
            for res in tools_response.tools_page:
                yield self._tool_from_response(res)

    def _tool_from_response(self, tool_response: ToolResponse) -> VoiceTool:
        return VoiceTool(
            id=tool_response.id,
            name=tool_response.name,
            created_on=tool_response.created_on,
            modified_on=tool_response.modified_on,
            parameters=tool_response.parameters,
            description=tool_response.description,
            fallback_content=tool_response.fallback_content,
        )

    def iter_tools(self) -> Iterator[VoiceTool]:
        """Iterate over existing EVI tools."""
        endpoint = self._build_endpoint("evi", "tools")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            tools_response = ToolsResponse.model_validate_json(response.text)
            if len(tools_response.tools_page) == 0:
                break
            for res in tools_response.tools_page:
                yield self._tool_from_response(res)

    def delete_tool(self, id: str, _version: Optional[int] = None) -> None:
        """Delete an EVI tool.

        Args:
            id (str): Tool ID.
        """
        route = f"tools/{id}" if _version is None else f"tools/{id}/version/{_version}"
        endpoint = self._build_endpoint("evi", route)
        self._request(endpoint, method="DELETE")
