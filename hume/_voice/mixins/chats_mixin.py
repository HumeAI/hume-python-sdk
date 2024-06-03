"""Client operations for managing EVI chats."""

import logging
from typing import Iterator

from hume._common.client_base import ClientBase
from hume._common.utilities.paging_utilities import Paging
from hume._voice.models.chats_models import (
    ChatEvent,
    ChatEventsResponse,
    ChatGroupEvent,
    ChatGroupEventsResponse,
    ChatGroupResponse,
    ChatGroupsResponse,
    ChatMessage,
    ChatResponse,
    ChatsResponse,
    VoiceChat,
    VoiceChatGroup,
)

logger = logging.getLogger(__name__)


# pylint: disable=redefined-builtin
class ChatsMixin(ClientBase):
    """Client operations for managing EVI chats."""

    def iter_chat_groups(self) -> Iterator[VoiceChatGroup]:
        """Iterate over existing EVI chat groups."""
        endpoint = self._build_endpoint("evi", "chat_groups")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            chats_response = ChatGroupsResponse.model_validate_json(response.text)
            if len(chats_response.chat_groups_page) == 0:
                break
            for res in chats_response.chat_groups_page:
                yield self._chat_group_from_response(res)

    def get_chat_group(self, id: str) -> VoiceChatGroup:
        """Get an EVI chat group by its ID.

        Args:
            id (str): Chat group ID.
        """
        endpoint = self._build_endpoint("evi", f"chat_groups/{id}")
        response = self._request(endpoint, method="GET")
        chats_response = ChatGroupResponse.model_validate_json(response.text)
        return self._chat_group_from_response(chats_response)

    def _chat_group_from_response(self, chat_group_response: ChatGroupResponse) -> VoiceChatGroup:
        return VoiceChatGroup(
            id=chat_group_response.id,
            first_start_timestamp=chat_group_response.first_start_timestamp,
            most_recent_start_timestamp=chat_group_response.most_recent_start_timestamp,
            num_chats=chat_group_response.num_chats,
            is_active=chat_group_response.is_active,
        )

    def iter_chat_group_messages(self, id: str) -> Iterator[ChatMessage]:
        """Iterate over chat messages for a given chat group ID.

        Args:
            id (str): Chat group ID.
        """
        endpoint = self._build_endpoint("evi", f"chat_groups/{id}/events")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            chat_group_events_response = ChatGroupEventsResponse.model_validate_json(response.text)
            if len(chat_group_events_response.events_page) == 0:
                break
            for chat_group_event in chat_group_events_response.events_page:
                yield self._chat_message_from_chat_group_event(chat_group_event)

    def _chat_message_from_chat_group_event(self, chat_group_event: ChatGroupEvent) -> ChatMessage:
        return ChatMessage(
            timestamp=chat_group_event.timestamp,
            role=chat_group_event.role,
            type=chat_group_event.type,
            message_text=chat_group_event.message_text,
            function_call=None,
            emotion_features=chat_group_event.emotion_features,
            metadata=chat_group_event.metadata,
        )

    def iter_chats(self) -> Iterator[VoiceChat]:
        """Iterate over existing EVI chats."""
        endpoint = self._build_endpoint("evi", "chats")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            chats_response = ChatsResponse.model_validate_json(response.text)
            if len(chats_response.chats_page) == 0:
                break
            for res in chats_response.chats_page:
                yield self._chat_from_response(res)

    def get_chat(self, id: str) -> VoiceChat:
        """Get an EVI chat by its ID.

        Args:
            id (str): Chat ID.
        """
        endpoint = self._build_endpoint("evi", f"chats/{id}")
        response = self._request(endpoint, method="GET")
        chats_response = ChatResponse.model_validate_json(response.text)
        return self._chat_from_response(chats_response)

    def _chat_from_response(self, chat_response: ChatResponse) -> VoiceChat:
        return VoiceChat(
            id=chat_response.id,
            chat_group_id=chat_response.chat_group_id,
            start_timestamp=chat_response.start_timestamp,
            end_timestamp=chat_response.end_timestamp,
        )

    def iter_chat_messages(self, id: str) -> Iterator[ChatMessage]:
        """Iterate over chat messages for a given chat ID.

        Args:
            id (str): Chat ID.
        """
        endpoint = self._build_endpoint("evi", f"chats/{id}")
        for page_number in range(self.PAGING_LIMIT):
            paging = Paging(page_size=self._page_size, page_number=page_number)
            response = self._request(endpoint, method="GET", paging=paging)
            chat_events_response = ChatEventsResponse.model_validate_json(response.text)
            if len(chat_events_response.events_page) == 0:
                break
            for chat_event in chat_events_response.events_page:
                yield self._chat_message_from_chat_event(chat_event)

    def _chat_message_from_chat_event(self, chat_event: ChatEvent) -> ChatMessage:
        return ChatMessage(
            timestamp=chat_event.timestamp,
            role=chat_event.role,
            type=chat_event.type,
            message_text=chat_event.message_text,
            function_call=chat_event.function_call,
            emotion_features=chat_event.emotion_features,
            metadata=chat_event.metadata,
        )
