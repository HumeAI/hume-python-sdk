# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .context import Context
from .audio_configuration import AudioConfiguration
from .tool import Tool
from .builtin_tool_config import BuiltinToolConfig
from .session_settings_variables_value import SessionSettingsVariablesValue
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class SessionSettings(UniversalBaseModel):
    """
    Settings for this chat session.
    """

    type: typing.Literal["session_settings"] = pydantic.Field(default="session_settings")
    """
    The type of message sent through the socket; must be `session_settings` for our server to correctly identify and process it as a Session Settings message.
    
    Session settings are temporary and apply only to the current Chat session. These settings can be adjusted dynamically based on the requirements of each session to ensure optimal performance and user experience.
    
    For more information, please refer to the [Session Settings guide](/docs/empathic-voice-interface-evi/configuration/session-settings).
    """

    custom_session_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Unique identifier for the session. Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    
    If included, the response sent from Hume to your backend will include this ID. This allows you to correlate frontend users with their incoming messages.
    
    It is recommended to pass a `custom_session_id` if you are using a Custom Language Model. Please see our guide to [using a custom language model](/docs/empathic-voice-interface-evi/guides/custom-language-model) with EVI to learn more.
    """

    system_prompt: typing.Optional[str] = pydantic.Field(default=None)
    """
    Instructions used to shape EVI’s behavior, responses, and style for the session.
    
    When included in a Session Settings message, the provided Prompt overrides the existing one specified in the EVI configuration. If no Prompt was defined in the configuration, this Prompt will be the one used for the session.
    
    You can use the Prompt to define a specific goal or role for EVI, specifying how it should act or what it should focus on during the conversation. For example, EVI can be instructed to act as a customer support representative, a fitness coach, or a travel advisor, each with its own set of behaviors and response styles.
    
    For help writing a system prompt, see our [Prompting Guide](/docs/empathic-voice-interface-evi/guides/prompting).
    """

    context: typing.Optional[Context] = pydantic.Field(default=None)
    """
    Allows developers to inject additional context into the conversation, which is appended to the end of user messages for the session.
    
    When included in a Session Settings message, the provided context can be used to remind the LLM of its role in every user message, prevent it from forgetting important details, or add new relevant information to the conversation.
    
    Set to `null` to disable context injection.
    """

    audio: typing.Optional[AudioConfiguration] = pydantic.Field(default=None)
    """
    Configuration details for the audio input used during the session. Ensures the audio is being correctly set up for processing.
    
    This optional field is only required when the audio input is encoded in PCM Linear 16 (16-bit, little-endian, signed PCM WAV data). For detailed instructions on how to configure session settings for PCM Linear 16 audio, please refer to the [Session Settings guide](/docs/empathic-voice-interface-evi/configuration/session-settings).
    """

    language_model_api_key: typing.Optional[str] = pydantic.Field(default=None)
    """
    Third party API key for the supplemental language model.
    
    When provided, EVI will use this key instead of Hume’s API key for the supplemental LLM. This allows you to bypass rate limits and utilize your own API key as needed.
    """

    tools: typing.Optional[typing.List[Tool]] = pydantic.Field(default=None)
    """
    List of user-defined tools to enable for the session.
    
    Tools are resources used by EVI to perform various tasks, such as searching the web or calling external APIs. Built-in tools, like web search, are natively integrated, while user-defined tools are created and invoked by the user. To learn more, see our [Tool Use Guide](/docs/empathic-voice-interface-evi/features/tool-use).
    """

    builtin_tools: typing.Optional[typing.List[BuiltinToolConfig]] = pydantic.Field(default=None)
    """
    List of built-in tools to enable for the session.
    
    Tools are resources used by EVI to perform various tasks, such as searching the web or calling external APIs. Built-in tools, like web search, are natively integrated, while user-defined tools are created and invoked by the user. To learn more, see our [Tool Use Guide](/docs/empathic-voice-interface-evi/features/tool-use).
    
    Currently, the only built-in tool Hume provides is **Web Search**. When enabled, Web Search equips EVI with the ability to search the web for up-to-date information.
    """

    metadata: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = None
    variables: typing.Optional[typing.Dict[str, SessionSettingsVariablesValue]] = pydantic.Field(default=None)
    """
    This field allows you to assign values to dynamic variables referenced in your system prompt.
    
    Each key represents the variable name, and the corresponding value is the specific content you wish to assign to that variable within the session. While the values for variables can be strings, numbers, or booleans, the value will ultimately be converted to a string when injected into your system prompt.
    
    Using this field, you can personalize responses based on session-specific details. For more guidance, see our [guide on using dynamic variables](/docs/empathic-voice-interface-evi/features/dynamic-variables).
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
