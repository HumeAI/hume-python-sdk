import logging
from typing import Iterator

from hume._common.client_base import ClientBase
from hume._common.utilities.paging_utilities import Paging
from hume._voice.models.chats_models import ChatEvent, ChatEventsResponse, ChatMessage

logger = logging.getLogger(__name__)


# pylint: disable=redefined-builtin
class ChatsMixin(ClientBase):
    def iter_chat_messages(self, id: str) -> Iterator[ChatMessage]:
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
