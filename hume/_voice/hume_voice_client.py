"""Empathic Voice Interface client."""

import logging

from hume._voice.mixins.chat_mixin import ChatMixin
from hume._voice.mixins.chats_mixin import ChatsMixin
from hume._voice.mixins.configs_mixin import ConfigsMixin
from hume._voice.mixins.tools_mixin import ToolsMixin

logger = logging.getLogger(__name__)


class HumeVoiceClient(ChatMixin, ChatsMixin, ConfigsMixin, ToolsMixin):
    """Empathic Voice Interface client."""
