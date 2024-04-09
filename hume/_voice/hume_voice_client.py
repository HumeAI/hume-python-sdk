"""Empathic Voice Interface client."""

import logging

from hume._voice.mixins.chat_mixin import ChatMixin
from hume._voice.mixins.chats_mixin import ChatsMixin
from hume._voice.mixins.configs_mixin import ConfigsMixin

logger = logging.getLogger(__name__)


class HumeVoiceClient(ChatMixin, ChatsMixin, ConfigsMixin):
    """Empathic Voice Interface client."""
