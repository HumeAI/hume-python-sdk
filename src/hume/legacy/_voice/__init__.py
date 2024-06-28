"""Module init."""

from hume.legacy._voice.hume_voice_client import HumeVoiceClient
from hume.legacy._voice.microphone.microphone_interface import MicrophoneInterface
from hume.legacy._voice.models.chats_models import VoiceChat
from hume.legacy._voice.models.configs_models import LanguageModelConfig, VoiceConfig, VoiceIdentityConfig
from hume.legacy._voice.models.tools_models import VoiceTool
from hume.legacy._voice.voice_socket import VoiceSocket

__all__ = [
    "HumeVoiceClient",
    "LanguageModelConfig",
    "MicrophoneInterface",
    "VoiceChat",
    "VoiceConfig",
    "VoiceIdentityConfig",
    "VoiceSocket",
    "VoiceTool",
]
