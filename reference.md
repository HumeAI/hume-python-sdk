# Reference
## EmpathicVoice ControlPlane
<details><summary><code>client.empathic_voice.control_plane.<a href="src/hume/empathic_voice/control_plane/client.py">send</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Send a message to a specific chat.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.empathic_voice import SessionSettings

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.control_plane.send(
    chat_id="chat_id",
    request=SessionSettings(
        type="session_settings",
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**chat_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request:** `ControlPlanePublishEvent` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EmpathicVoice ChatGroups
<details><summary><code>client.empathic_voice.chat_groups.<a href="src/hume/empathic_voice/chat_groups/client.py">list_chat_groups</a>(...) -> ReturnPagedChatGroups</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Chat Groups**.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chat_groups.list_chat_groups(
    page_number=0,
    page_size=1,
    ascending_order=True,
    config_id="your-config-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` — Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**config_id:** `typing.Optional[str]` 

The unique identifier for an EVI configuration.

Filter Chat Groups to only include Chats that used this `config_id` in their most recent Chat.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.chat_groups.<a href="src/hume/empathic_voice/chat_groups/client.py">get_chat_group</a>(...) -> ReturnChatGroupPagedChats</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a **ChatGroup** by ID, including a paginated list of **Chats** associated with the **ChatGroup**.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chat_groups.get_chat_group(
    id="your-chat-group-id",
    page_number=0,
    page_size=1,
    ascending_order=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Chat Group. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[str]` — Chat status to apply to the chat. String from the ChatStatus enum.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` — Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.chat_groups.<a href="src/hume/empathic_voice/chat_groups/client.py">get_audio</a>(...) -> ReturnChatGroupPagedAudioReconstructions</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of audio for each **Chat** within the specified **Chat Group**. For more details, see our guide on audio reconstruction [here](/docs/speech-to-speech-evi/faq#can-i-access-the-audio-of-previous-conversations-with-evi).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chat_groups.get_audio(
    id="your-chat-group-id",
    page_number=0,
    page_size=10,
    ascending_order=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Chat Group. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` — Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.chat_groups.<a href="src/hume/empathic_voice/chat_groups/client.py">list_chat_group_events</a>(...) -> ReturnChatGroupPagedEvents</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Chat** events associated with a **Chat Group**.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chat_groups.list_chat_group_events(
    id="your-chat-group-id",
    page_number=0,
    page_size=3,
    ascending_order=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Chat Group. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` — Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EmpathicVoice Chats
<details><summary><code>client.empathic_voice.chats.<a href="src/hume/empathic_voice/chats/client.py">list_chats</a>(...) -> ReturnPagedChats</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Chats**.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chats.list_chats(
    page_number=0,
    page_size=1,
    ascending_order=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` — Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**config_id:** `typing.Optional[str]` — Filter to only include chats that used this config.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[str]` — Chat status to apply to the chat. String from the ChatStatus enum.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.chats.<a href="src/hume/empathic_voice/chats/client.py">list_chat_events</a>(...) -> ReturnChatPagedEvents</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Chat** events.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chats.list_chat_events(
    id="your-chat-id",
    page_number=0,
    page_size=3,
    ascending_order=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Chat. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` — Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.chats.<a href="src/hume/empathic_voice/chats/client.py">get_audio</a>(...) -> ReturnChatAudioReconstruction</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches the audio of a previous **Chat**. For more details, see our guide on audio reconstruction [here](/docs/speech-to-speech-evi/faq#can-i-access-the-audio-of-previous-conversations-with-evi).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.chats.get_audio(
    id="your-chat-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Chat. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EmpathicVoice Configs
<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">list_configs</a>(...) -> ReturnPagedConfigs</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Configs**.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.list_configs(
    page_number=0,
    page_size=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each config. To include all versions of each config in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Filter to only include configs with this name.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">create_config</a>(...) -> ReturnConfig</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a **Config** which can be applied to EVI.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.empathic_voice import PostedConfigPromptSpec, VoiceName, PostedLanguageModel, PostedEventMessageSpecs, PostedEventMessageSpec

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.create_config(
    name="Weather Assistant Config",
    prompt=PostedConfigPromptSpec(
        id="",
        version=0,
    ),
    evi_version="3",
    voice=VoiceName(
        provider="HUME_AI",
        name="Ava Song",
    ),
    language_model=PostedLanguageModel(
        model_provider="ANTHROPIC",
        model_resource="claude-3-7-sonnet-latest",
        temperature=1,
    ),
    event_messages=PostedEventMessageSpecs(
        on_new_chat=PostedEventMessageSpec(
            enabled=False,
            text="",
        ),
        on_inactivity_timeout=PostedEventMessageSpec(
            enabled=False,
            text="",
        ),
        on_max_duration_timeout=PostedEventMessageSpec(
            enabled=False,
            text="",
        ),
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**evi_version:** `str` — EVI version to use. Only versions `3` and `4-mini` are supported.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — Name applied to all versions of a particular Config.
    
</dd>
</dl>

<dl>
<dd>

**builtin_tools:** `typing.Optional[typing.List[typing.Optional[PostedBuiltinTool]]]` — Built-in tool specification for a Config.
    
</dd>
</dl>

<dl>
<dd>

**ellm_model:** `typing.Optional[PostedEllmModel]` 
    
</dd>
</dl>

<dl>
<dd>

**event_messages:** `typing.Optional[PostedEventMessageSpecs]` 
    
</dd>
</dl>

<dl>
<dd>

**interruption:** `typing.Optional[PostedInterruptionSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**language_model:** `typing.Optional[PostedLanguageModel]` 
    
</dd>
</dl>

<dl>
<dd>

**nudges:** `typing.Optional[PostedNudgeSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[PostedConfigPromptSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**timeouts:** `typing.Optional[PostedTimeoutSpecs]` 
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.List[typing.Optional[PostedUserDefinedToolSpec]]]` — Tool specification for a Config.
    
</dd>
</dl>

<dl>
<dd>

**turn_detection:** `typing.Optional[PostedTurnDetectionSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Config version.
    
</dd>
</dl>

<dl>
<dd>

**voice:** `typing.Optional[VoiceRef]` — A voice specification associated with this Config.
    
</dd>
</dl>

<dl>
<dd>

**webhooks:** `typing.Optional[typing.List[typing.Optional[PostedWebhookSpec]]]` — Webhook config specifications for each subscriber.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">list_config_versions</a>(...) -> ReturnPagedConfigs</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a list of a **Config's** versions.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.list_config_versions(
    id="your-config-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each config. To include all versions of each config in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">create_config_version</a>(...) -> ReturnConfig</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a **Config** by creating a new version of the **Config**.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.empathic_voice import PostedConfigPromptSpec, VoiceName, PostedLanguageModel, PostedEllmModel, PostedEventMessageSpecs, PostedEventMessageSpec

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.create_config_version(
    id="your-config-id",
    version_description="This is an updated version of the Weather Assistant Config.",
    evi_version="3",
    prompt=PostedConfigPromptSpec(
        id="",
        version=0,
    ),
    voice=VoiceName(
        provider="HUME_AI",
        name="Ava Song",
    ),
    language_model=PostedLanguageModel(
        model_provider="ANTHROPIC",
        model_resource="claude-3-7-sonnet-latest",
        temperature=1,
    ),
    ellm_model=PostedEllmModel(
        allow_short_responses=True,
    ),
    event_messages=PostedEventMessageSpecs(
        on_new_chat=PostedEventMessageSpec(
            enabled=False,
            text="",
        ),
        on_inactivity_timeout=PostedEventMessageSpec(
            enabled=False,
            text="",
        ),
        on_max_duration_timeout=PostedEventMessageSpec(
            enabled=False,
            text="",
        ),
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**evi_version:** `str` — EVI version to use. Only versions `3` and `4-mini` are supported.
    
</dd>
</dl>

<dl>
<dd>

**builtin_tools:** `typing.Optional[typing.List[typing.Optional[PostedBuiltinTool]]]` — Built-in tool specification for a Config.
    
</dd>
</dl>

<dl>
<dd>

**ellm_model:** `typing.Optional[PostedEllmModel]` 
    
</dd>
</dl>

<dl>
<dd>

**event_messages:** `typing.Optional[PostedEventMessageSpecs]` 
    
</dd>
</dl>

<dl>
<dd>

**interruption:** `typing.Optional[PostedInterruptionSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**language_model:** `typing.Optional[PostedLanguageModel]` 
    
</dd>
</dl>

<dl>
<dd>

**nudges:** `typing.Optional[PostedNudgeSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[PostedConfigPromptSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**timeouts:** `typing.Optional[PostedTimeoutSpecs]` 
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.List[typing.Optional[PostedUserDefinedToolSpec]]]` — Tool specification for a Config.
    
</dd>
</dl>

<dl>
<dd>

**turn_detection:** `typing.Optional[PostedTurnDetectionSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Config version.
    
</dd>
</dl>

<dl>
<dd>

**voice:** `typing.Optional[VoiceRef]` 
    
</dd>
</dl>

<dl>
<dd>

**webhooks:** `typing.Optional[typing.List[typing.Optional[PostedWebhookSpec]]]` — Webhook config specifications for each subscriber.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">delete_config</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a **Config** and its versions.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.delete_config(
    id="your-config-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">update_config_name</a>(...) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the name of a **Config**.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.update_config_name(
    id="your-config-id",
    name="Updated Weather Assistant Config Name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — Name applied to all versions of a particular Config.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">get_config_version</a>(...) -> ReturnConfig</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a specified version of a **Config**.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.get_config_version(
    id="your-config-id",
    version=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Config.

Configs, Prompts, Custom Voices, and Tools are versioned. This versioning system supports iterative development, allowing you to progressively refine configurations and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Config. Each update to the Config increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">delete_config_version</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a specified version of a **Config**.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.delete_config_version(
    id="your-config-id",
    version=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Config.

Configs, Prompts, Custom Voices, and Tools are versioned. This versioning system supports iterative development, allowing you to progressively refine configurations and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Config. Each update to the Config increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">update_config_description</a>(...) -> ReturnConfig</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the description of a **Config**.

For more details on configuration options and how to configure EVI, see our [configuration guide](/docs/speech-to-speech-evi/configuration).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.configs.update_config_description(
    id="your-config-id",
    version=1,
    version_description="This is an updated version_description.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Config. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Config.

Configs, Prompts, Custom Voices, and Tools are versioned. This versioning system supports iterative development, allowing you to progressively refine configurations and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Config. Each update to the Config increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Config version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EmpathicVoice Prompts
<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">list_prompts</a>(...) -> ReturnPagedPrompts</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Prompts**.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.list_prompts(
    page_number=0,
    page_size=2,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each prompt. To include all versions of each prompt in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Filter to only include prompts with name.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">create_prompt</a>(...) -> typing.Optional[ReturnPrompt]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a **Prompt** that can be added to an [EVI configuration](/reference/speech-to-speech-evi/configs/create-config).

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.create_prompt(
    name="Weather Assistant Prompt",
    text="<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name applied to all versions of a particular Prompt.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` 

Instructions used to shape EVI's behavior, responses, and style.

You can use the Prompt to define a specific goal or role for EVI, specifying how it should act or what it should focus on during the conversation. For example, EVI can be instructed to act as a customer support representative, a fitness coach, or a travel advisor, each with its own set of behaviors and response styles. For help writing a system prompt, see our [Prompting Guide](/docs/speech-to-speech-evi/guides/prompting).
    
</dd>
</dl>

<dl>
<dd>

**prompt_expansion:** `typing.Optional[PromptExpansionSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Prompt version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">list_prompt_versions</a>(...) -> ReturnPagedPrompts</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a list of a **Prompt's** versions.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.list_prompt_versions(
    id="your-prompt-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each prompt. To include all versions of each prompt in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">create_prompt_version</a>(...) -> typing.Optional[ReturnPrompt]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a **Prompt** by creating a new version of the **Prompt**.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.create_prompt_version(
    id="your-prompt-id",
    text="<role>You are an updated version of an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
    version_description="This is an updated version of the Weather Assistant Prompt.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Prompt. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` 

Instructions used to shape EVI's behavior, responses, and style.

You can use the Prompt to define a specific goal or role for EVI, specifying how it should act or what it should focus on during the conversation. For example, EVI can be instructed to act as a customer support representative, a fitness coach, or a travel advisor, each with its own set of behaviors and response styles. For help writing a system prompt, see our [Prompting Guide](/docs/speech-to-speech-evi/guides/prompting).
    
</dd>
</dl>

<dl>
<dd>

**prompt_expansion:** `typing.Optional[PromptExpansionSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Prompt version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">delete_prompt</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a **Prompt** and its versions.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.delete_prompt(
    id="your-prompt-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Prompt. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">update_prompt_name</a>(...) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the name of a **Prompt**.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.update_prompt_name(
    id="your-prompt-id",
    name="Updated Weather Assistant Prompt Name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Prompt. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — Name applied to all versions of a particular Prompt.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">get_prompt_version</a>(...) -> typing.Optional[ReturnPrompt]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a specified version of a **Prompt**.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.get_prompt_version(
    id="your-prompt-id",
    version=0,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Prompt. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Prompt.

Prompts, Configs, Custom Voices, and Tools are versioned. This versioning system supports iterative development, allowing you to progressively refine prompts and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Prompt. Each update to the Prompt increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">delete_prompt_version</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a specified version of a **Prompt**.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.delete_prompt_version(
    id="your-prompt-id",
    version=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Prompt. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Prompt.

Prompts, Configs, Custom Voices, and Tools are versioned. This versioning system supports iterative development, allowing you to progressively refine prompts and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Prompt. Each update to the Prompt increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">update_prompt_description</a>(...) -> typing.Optional[ReturnPrompt]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the description of a **Prompt**.

See our [prompting guide](/docs/speech-to-speech-evi/guides/phone-calling) for tips on crafting your system prompt.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.prompts.update_prompt_description(
    id="your-prompt-id",
    version=1,
    version_description="This is an updated version_description.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Prompt. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Prompt.

Prompts, Configs, Custom Voices, and Tools are versioned. This versioning system supports iterative development, allowing you to progressively refine prompts and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Prompt. Each update to the Prompt increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Prompt version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## EmpathicVoice Tools
<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">list_tools</a>(...) -> ReturnPagedUserDefinedTools</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Tools**.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.list_tools(
    page_number=0,
    page_size=2,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each tool. To include all versions of each tool in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Filter to only include tools with name.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">create_tool</a>(...) -> typing.Optional[ReturnUserDefinedTool]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a **Tool** that can be added to an [EVI configuration](/reference/speech-to-speech-evi/configs/create-config).

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.create_tool(
    name="get_current_weather",
    parameters="{ \"type\": \"object\", \"properties\": { \"location\": { \"type\": \"string\", \"description\": \"The city and state, e.g. San Francisco, CA\" }, \"format\": { \"type\": \"string\", \"enum\": [\"celsius\", \"fahrenheit\"], \"description\": \"The temperature unit to use. Infer this from the users location.\" } }, \"required\": [\"location\", \"format\"] }",
    version_description="Fetches current weather and uses celsius or fahrenheit based on location of user.",
    description="This tool is for getting the current weather.",
    fallback_content="Unable to fetch current weather.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` 

Name of the built-in tool to use. Hume supports the following built-in tools:

- **web_search:** enables EVI to search the web for up-to-date information when applicable.
- **hang_up:** closes the WebSocket connection when appropriate (e.g., after detecting a farewell in the conversation).

For more information, see our guide on [using built-in tools](/docs/speech-to-speech-evi/features/tool-use#using-built-in-tools).
    
</dd>
</dl>

<dl>
<dd>

**parameters:** `str` 

Stringified JSON defining the parameters used by this version of the Tool.

These parameters define the inputs needed for the Tool's execution, including the expected data type and description for each input field. Structured as a stringified JSON schema, this format ensures the Tool receives data in the expected format.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of what the Tool does, used by the supplemental LLM to choose when and how to call the function.
    
</dd>
</dl>

<dl>
<dd>

**fallback_content:** `typing.Optional[str]` — Optional text passed to the supplemental LLM in place of the tool call result. The LLM then uses this text to generate a response back to the user, ensuring continuity in the conversation if the Tool errors.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Tool version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">list_tool_versions</a>(...) -> ReturnPagedUserDefinedTools</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a list of a **Tool's** versions.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.list_tool_versions(
    id="your-tool-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each tool. To include all versions of each tool in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">create_tool_version</a>(...) -> typing.Optional[ReturnUserDefinedTool]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a **Tool** by creating a new version of the **Tool**.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.create_tool_version(
    id="your-tool-id",
    parameters="{ \"type\": \"object\", \"properties\": { \"location\": { \"type\": \"string\", \"description\": \"The city and state, e.g. San Francisco, CA\" }, \"format\": { \"type\": \"string\", \"enum\": [\"celsius\", \"fahrenheit\", \"kelvin\"], \"description\": \"The temperature unit to use. Infer this from the users location.\" } }, \"required\": [\"location\", \"format\"] }",
    version_description="Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
    fallback_content="Unable to fetch current weather.",
    description="This tool is for getting the current weather.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Tool. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**parameters:** `str` 

Stringified JSON defining the parameters used by this version of the Tool.

These parameters define the inputs needed for the Tool's execution, including the expected data type and description for each input field. Structured as a stringified JSON schema, this format ensures the Tool receives data in the expected format.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of what the Tool does, used by the supplemental LLM to choose when and how to call the function.
    
</dd>
</dl>

<dl>
<dd>

**fallback_content:** `typing.Optional[str]` — Optional text passed to the supplemental LLM in place of the tool call result. The LLM then uses this text to generate a response back to the user, ensuring continuity in the conversation if the Tool errors.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Tool version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">delete_tool</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a **Tool** and its versions.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.delete_tool(
    id="your-tool-id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Tool. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">update_tool_name</a>(...) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the name of a **Tool**.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.update_tool_name(
    id="your-tool-id",
    name="get_current_temperature",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Tool. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 

Name of the built-in tool to use. Hume supports the following built-in tools:

- **web_search:** enables EVI to search the web for up-to-date information when applicable.
- **hang_up:** closes the WebSocket connection when appropriate (e.g., after detecting a farewell in the conversation).

For more information, see our guide on [using built-in tools](/docs/speech-to-speech-evi/features/tool-use#using-built-in-tools).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">get_tool_version</a>(...) -> typing.Optional[ReturnUserDefinedTool]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a specified version of a **Tool**.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.get_tool_version(
    id="your-tool-id",
    version=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Tool. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Tool.

Tools, Configs, Custom Voices, and Prompts are versioned. This versioning system supports iterative development, allowing you to progressively refine tools and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Tool. Each update to the Tool increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">delete_tool_version</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a specified version of a **Tool**.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.delete_tool_version(
    id="",
    version=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Tool. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Tool.

Tools, Configs, Custom Voices, and Prompts are versioned. This versioning system supports iterative development, allowing you to progressively refine tools and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Tool. Each update to the Tool increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">update_tool_description</a>(...) -> typing.Optional[ReturnUserDefinedTool]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the description of a specified **Tool** version.

Refer to our [tool use](/docs/speech-to-speech-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.empathic_voice.tools.update_tool_description(
    id="your-tool-id",
    version=1,
    version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user\'s region.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Identifier for a Tool. Formatted as a UUID.
    
</dd>
</dl>

<dl>
<dd>

**version:** `int` 

Version number for a Tool.

Tools, Configs, Custom Voices, and Prompts are versioned. This versioning system supports iterative development, allowing you to progressively refine tools and revert to previous versions if needed.

Version numbers are integer values representing different iterations of the Tool. Each update to the Tool increments its version number.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Tool version.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tts Voices
<details><summary><code>client.tts.voices.<a href="src/hume/tts/voices/client.py">list</a>(...) -> ReturnPagedVoices</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists voices you have saved in your account, or voices from the [Voice Library](https://app.hume.ai/tts/voice-library).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.voices.list(
    provider="CUSTOM_VOICE",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**provider:** `VoiceProvider` 

Specify the voice provider to filter voices returned by the endpoint:

- **`HUME_AI`**: Lists preset, shared voices from Hume's [Voice Library](https://app.hume.ai/tts/voice-library).
- **`CUSTOM_VOICE`**: Lists custom voices created and saved to your account.
    
</dd>
</dl>

<dl>
<dd>

**page_number:** `typing.Optional[int]` 

Specifies the page number to retrieve, enabling pagination.

This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` 

Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.
    
</dd>
</dl>

<dl>
<dd>

**ascending_order:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**filter_tag:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 

Filter voices by tag using `TAG:TAG_VALUE` syntax.

For example, `GENDER:Male` returns only voices with the `GENDER` tag set to `Male`. Tag types are case-insensitive; tag values are case-sensitive.

Multiple values are ANDed together; for example, `[GENDER:Male, LANGUAGE:Japanese]` returns only voices matching both criteria.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.voices.<a href="src/hume/tts/voices/client.py">create</a>(...) -> ReturnVoice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Saves a new custom voice to your account using the specified TTS generation ID.

Once saved, this voice can be reused in subsequent TTS requests, ensuring consistent speech style and prosody. For more details on voice creation, see the [Voices Guide](/docs/text-to-speech-tts/voices).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.voices.create(
    generation_id="",
    name="David Hume",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**generation_id:** `str` — A unique ID associated with this TTS generation that can be used as context for generating consistent speech style and prosody across multiple requests.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of a **Voice**.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.voices.<a href="src/hume/tts/voices/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a previously generated custom voice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.voices.delete(
    name="David Hume",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name of the voice to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tts
<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_json</a>(...) -> ReturnTts</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesizes one or more input texts into speech using the specified voice. If no voice is provided, a novel voice will be generated dynamically. Optionally, additional context can be included to influence the speech's style and prosody.

The response includes the base64-encoded audio and metadata in JSON format.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.tts import PostedContextWithUtterances, PostedUtterance, FormatMp3

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.synthesize_json(
    context=PostedContextWithUtterances(
        utterances=[
            PostedUtterance(
                text="How can people see beauty so differently?",
                description="A curious student with a clear and respectful tone, seeking clarification on Hume\'s ideas with a straightforward question.",
            )
        ],
    ),
    format=FormatMp3(
        type="mp3",
    ),
    num_generations=1,
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `PostedTts` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_file</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Synthesizes one or more input texts into speech using the specified voice. If no voice is provided, a novel voice will be generated dynamically. Optionally, additional context can be included to influence the speech's style and prosody. 

The response contains the generated audio file in the requested format.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.tts import PostedContextWithGenerationId, FormatMp3, PostedUtterance

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.synthesize_file(
    context=PostedContextWithGenerationId(
        generation_id="",
    ),
    format=FormatMp3(
        type="mp3",
    ),
    num_generations=1,
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `PostedTts` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_file_streaming</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Streams synthesized speech using the specified voice. If no voice is provided, a novel voice will be generated dynamically. Optionally, additional context can be included to influence the speech's style and prosody.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.tts import PostedUtterance, PostedUtteranceVoiceWithName

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.synthesize_file_streaming(
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            voice=PostedUtteranceVoiceWithName(
                name="Male English Actor",
                provider="HUME_AI",
            ),
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `PostedTts` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_json_streaming</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Streams synthesized speech using the specified voice. If no voice is provided, a novel voice will be generated dynamically. Optionally, additional context can be included to influence the speech's style and prosody. 

The response is a stream of JSON objects including audio encoded in base64.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment
from hume.tts import PostedUtterance, PostedUtteranceVoiceWithName

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.synthesize_json_streaming(
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            voice=PostedUtteranceVoiceWithName(
                name="Male English Actor",
                provider="HUME_AI",
            ),
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `PostedTts` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">convert_voice_file</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
client.tts.convert_voice_file(...)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**audio:** `core.File` — Audio file containing speech to be converted to the target voice. Supported formats include `MP3`, `WAV`, `M4A`, and `OGG`.
    
</dd>
</dl>

<dl>
<dd>

**strip_headers:** `typing.Optional[bool]` — If enabled, the audio for all the chunks of a generation, once concatenated together, will constitute a single audio file. Otherwise, if disabled, each chunk's audio will be its own audio file, each with its own headers (if applicable).
    
</dd>
</dl>

<dl>
<dd>

**context:** `typing.Optional[PostedContext]` — Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    
</dd>
</dl>

<dl>
<dd>

**voice:** `typing.Optional[PostedUtteranceVoice]` 
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[Format]` — Specifies the output audio file format.
    
</dd>
</dl>

<dl>
<dd>

**include_timestamp_types:** `typing.Optional[typing.List[TimestampType]]` — The set of timestamp types to include in the response. When used in multipart/form-data, specify each value using bracket notation: `include_timestamp_types[0]=word&include_timestamp_types[1]=phoneme`. Only supported for Octave 2 requests.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">convert_voice_json</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.tts.convert_voice_json(
    audio="example_audio",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**strip_headers:** `typing.Optional[bool]` — If enabled, the audio for all the chunks of a generation, once concatenated together, will constitute a single audio file. Otherwise, if disabled, each chunk's audio will be its own audio file, each with its own headers (if applicable).
    
</dd>
</dl>

<dl>
<dd>

**audio:** `typing.Optional[core.File]` — Audio file containing speech to be converted to the target voice. Supported formats include `MP3`, `WAV`, `M4A`, and `OGG`.
    
</dd>
</dl>

<dl>
<dd>

**context:** `typing.Optional[PostedContext]` — Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    
</dd>
</dl>

<dl>
<dd>

**voice:** `typing.Optional[PostedUtteranceVoice]` 
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[Format]` — Specifies the output audio file format.
    
</dd>
</dl>

<dl>
<dd>

**include_timestamp_types:** `typing.Optional[typing.List[TimestampType]]` — The set of timestamp types to include in the response. When used in multipart/form-data, specify each value using bracket notation: `include_timestamp_types[0]=word&include_timestamp_types[1]=phoneme`. Only supported for Octave 2 requests.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ExpressionMeasurement Batch
<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">list_jobs</a>(...) -> typing.List[UnionJob]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Sort and filter jobs.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.expression_measurement.batch.list_jobs()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The maximum number of jobs to include in the response.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[typing.Union[Status, typing.Sequence[Status]]]` 

Include only jobs of this status in the response. There are four possible statuses:

- `QUEUED`: The job has been received and is waiting to be processed.

- `IN_PROGRESS`: The job is currently being processed. 

- `COMPLETED`: The job has finished processing.

- `FAILED`: The job encountered an error and could not be completed successfully.
    
</dd>
</dl>

<dl>
<dd>

**when:** `typing.Optional[When]` — Specify whether to include jobs created before or after a given `timestamp_ms`.
    
</dd>
</dl>

<dl>
<dd>

**timestamp_ms:** `typing.Optional[int]` 

Provide a timestamp in milliseconds to filter jobs.

 When combined with the `when` parameter, you can filter jobs before or after the given timestamp. Defaults to the current Unix timestamp if one is not provided.
    
</dd>
</dl>

<dl>
<dd>

**sort_by:** `typing.Optional[SortBy]` 

Specify which timestamp to sort the jobs by.

- `created`: Sort jobs by the time of creation, indicated by `created_timestamp_ms`.

- `started`: Sort jobs by the time processing started, indicated by `started_timestamp_ms`.

- `ended`: Sort jobs by the time processing ended, indicated by `ended_timestamp_ms`.
    
</dd>
</dl>

<dl>
<dd>

**direction:** `typing.Optional[Direction]` 

Specify the order in which to sort the jobs. Defaults to descending order.

- `asc`: Sort in ascending order (chronological, with the oldest records first).

- `desc`: Sort in descending order (reverse-chronological, with the newest records first).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">start_inference_job</a>(...) -> JobId</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start a new measurement inference job.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.expression_measurement.batch.start_inference_job(
    urls=[
        "https://hume-tutorials.s3.amazonaws.com/faces.zip"
    ],
    notify=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `InferenceBaseRequest` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">get_job_details</a>(...) -> UnionJob</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the request details and state of a given job.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.expression_measurement.batch.get_job_details(
    id="job_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier for the job.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">get_job_predictions</a>(...) -> typing.List[UnionPredictResult]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the JSON predictions of a completed inference job.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.expression_measurement.batch.get_job_predictions(
    id="job_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier for the job.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">get_job_artifacts</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the artifacts ZIP of a completed inference job.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
client.expression_measurement.batch.get_job_artifacts(...)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique identifier for the job.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">start_inference_job_from_local_file</a>(...) -> JobId</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start a new batch inference job.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume import HumeClient
from hume.environment import HumeClientEnvironment

client = HumeClient(
    api_key="<value>",
    environment=HumeClientEnvironment.PROD,
)

client.expression_measurement.batch.start_inference_job()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**file:** `typing.List[core.File]` 

Local media files (see recommended input filetypes) to be processed.

If you wish to supply more than 100 files, consider providing them as an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`).
    
</dd>
</dl>

<dl>
<dd>

**json:** `typing.Optional[InferenceBaseRequest]` — Stringified JSON object containing the inference job configuration.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

