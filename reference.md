# Reference
## Tts
<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_json</a>(...)</code></summary>
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
from hume.tts import FormatMp3, PostedContextWithUtterances, PostedUtterance

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.tts.synthesize_json(
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
        )
    ],
    context=PostedContextWithUtterances(
        utterances=[
            PostedUtterance(
                text="How can people see beauty so differently?",
                description="A curious student with a clear and respectful tone, seeking clarification on Hume's ideas with a straightforward question.",
            )
        ],
    ),
    format=FormatMp3(),
    num_generations=1,
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

**utterances:** `typing.Sequence[PostedUtterance]` 

A list of **Utterances** to be converted to speech output.

An **Utterance** is a unit of input for [Octave](/docs/text-to-speech-tts/overview), and includes input `text`, an optional `description` to serve as the prompt for how the speech should be delivered, an optional `voice` specification, and additional controls to guide delivery for `speed` and `trailing_silence`.
    
</dd>
</dl>

<dl>
<dd>

**context:** `typing.Optional[PostedContext]` — Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[Format]` — Specifies the output audio file format.
    
</dd>
</dl>

<dl>
<dd>

**num_generations:** `typing.Optional[int]` — Number of generations of the audio to produce.
    
</dd>
</dl>

<dl>
<dd>

**split_utterances:** `typing.Optional[bool]` 

Controls how audio output is segmented in the response.

- When **enabled** (`true`), input utterances are automatically split into natural-sounding speech segments.

- When **disabled** (`false`), the response maintains a strict one-to-one mapping between input utterances and output snippets. 

This setting affects how the `snippets` array is structured in the response, which may be important for applications that need to track the relationship between input text and generated audio segments. When setting to `false`, avoid including utterances with long `text`, as this can result in distorted output.
    
</dd>
</dl>

<dl>
<dd>

**strip_headers:** `typing.Optional[bool]` — If enabled, the audio for all the chunks of a generation, once concatenated together, will constitute a single audio file. Otherwise, if disabled, each chunk's audio will be its own audio file, each with its own headers (if applicable).
    
</dd>
</dl>

<dl>
<dd>

**instant_mode:** `typing.Optional[bool]` 

Enables ultra-low latency streaming, significantly reducing the time until the first audio chunk is received. Recommended for real-time applications requiring immediate audio playback. For further details, see our documentation on [instant mode](/docs/text-to-speech-tts/overview#ultra-low-latency-streaming-instant-mode). 
- Dynamic voice generation is not supported with this mode; a predefined [voice](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.utterances.voice) must be specified in your request.
- This mode is only supported for streaming endpoints (e.g., [/v0/tts/stream/json](/reference/text-to-speech-tts/synthesize-json-streaming), [/v0/tts/stream/file](/reference/text-to-speech-tts/synthesize-file-streaming)).
- Ensure only a single generation is requested ([num_generations](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.num_generations) must be `1` or omitted).
- With `instant_mode` enabled, **requests incur a 10% higher cost** due to increased compute and resource requirements.
    
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

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_file</a>(...)</code></summary>
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
from hume.tts import FormatMp3, PostedContextWithGenerationId, PostedUtterance

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.tts.synthesize_file(
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
        )
    ],
    context=PostedContextWithGenerationId(
        generation_id="09ad914d-8e7f-40f8-a279-e34f07f7dab2",
    ),
    format=FormatMp3(),
    num_generations=1,
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

**utterances:** `typing.Sequence[PostedUtterance]` 

A list of **Utterances** to be converted to speech output.

An **Utterance** is a unit of input for [Octave](/docs/text-to-speech-tts/overview), and includes input `text`, an optional `description` to serve as the prompt for how the speech should be delivered, an optional `voice` specification, and additional controls to guide delivery for `speed` and `trailing_silence`.
    
</dd>
</dl>

<dl>
<dd>

**context:** `typing.Optional[PostedContext]` — Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[Format]` — Specifies the output audio file format.
    
</dd>
</dl>

<dl>
<dd>

**num_generations:** `typing.Optional[int]` — Number of generations of the audio to produce.
    
</dd>
</dl>

<dl>
<dd>

**split_utterances:** `typing.Optional[bool]` 

Controls how audio output is segmented in the response.

- When **enabled** (`true`), input utterances are automatically split into natural-sounding speech segments.

- When **disabled** (`false`), the response maintains a strict one-to-one mapping between input utterances and output snippets. 

This setting affects how the `snippets` array is structured in the response, which may be important for applications that need to track the relationship between input text and generated audio segments. When setting to `false`, avoid including utterances with long `text`, as this can result in distorted output.
    
</dd>
</dl>

<dl>
<dd>

**strip_headers:** `typing.Optional[bool]` — If enabled, the audio for all the chunks of a generation, once concatenated together, will constitute a single audio file. Otherwise, if disabled, each chunk's audio will be its own audio file, each with its own headers (if applicable).
    
</dd>
</dl>

<dl>
<dd>

**instant_mode:** `typing.Optional[bool]` 

Enables ultra-low latency streaming, significantly reducing the time until the first audio chunk is received. Recommended for real-time applications requiring immediate audio playback. For further details, see our documentation on [instant mode](/docs/text-to-speech-tts/overview#ultra-low-latency-streaming-instant-mode). 
- Dynamic voice generation is not supported with this mode; a predefined [voice](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.utterances.voice) must be specified in your request.
- This mode is only supported for streaming endpoints (e.g., [/v0/tts/stream/json](/reference/text-to-speech-tts/synthesize-json-streaming), [/v0/tts/stream/file](/reference/text-to-speech-tts/synthesize-file-streaming)).
- Ensure only a single generation is requested ([num_generations](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.num_generations) must be `1` or omitted).
- With `instant_mode` enabled, **requests incur a 10% higher cost** due to increased compute and resource requirements.
    
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

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_file_streaming</a>(...)</code></summary>
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
from hume.tts import FormatMp3, PostedContextWithGenerationId, PostedUtterance

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.tts.synthesize_file_streaming(
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
        )
    ],
    context=PostedContextWithGenerationId(
        generation_id="09ad914d-8e7f-40f8-a279-e34f07f7dab2",
    ),
    format=FormatMp3(),
    num_generations=1,
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

**utterances:** `typing.Sequence[PostedUtterance]` 

A list of **Utterances** to be converted to speech output.

An **Utterance** is a unit of input for [Octave](/docs/text-to-speech-tts/overview), and includes input `text`, an optional `description` to serve as the prompt for how the speech should be delivered, an optional `voice` specification, and additional controls to guide delivery for `speed` and `trailing_silence`.
    
</dd>
</dl>

<dl>
<dd>

**context:** `typing.Optional[PostedContext]` — Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[Format]` — Specifies the output audio file format.
    
</dd>
</dl>

<dl>
<dd>

**num_generations:** `typing.Optional[int]` — Number of generations of the audio to produce.
    
</dd>
</dl>

<dl>
<dd>

**split_utterances:** `typing.Optional[bool]` 

Controls how audio output is segmented in the response.

- When **enabled** (`true`), input utterances are automatically split into natural-sounding speech segments.

- When **disabled** (`false`), the response maintains a strict one-to-one mapping between input utterances and output snippets. 

This setting affects how the `snippets` array is structured in the response, which may be important for applications that need to track the relationship between input text and generated audio segments. When setting to `false`, avoid including utterances with long `text`, as this can result in distorted output.
    
</dd>
</dl>

<dl>
<dd>

**strip_headers:** `typing.Optional[bool]` — If enabled, the audio for all the chunks of a generation, once concatenated together, will constitute a single audio file. Otherwise, if disabled, each chunk's audio will be its own audio file, each with its own headers (if applicable).
    
</dd>
</dl>

<dl>
<dd>

**instant_mode:** `typing.Optional[bool]` 

Enables ultra-low latency streaming, significantly reducing the time until the first audio chunk is received. Recommended for real-time applications requiring immediate audio playback. For further details, see our documentation on [instant mode](/docs/text-to-speech-tts/overview#ultra-low-latency-streaming-instant-mode). 
- Dynamic voice generation is not supported with this mode; a predefined [voice](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.utterances.voice) must be specified in your request.
- This mode is only supported for streaming endpoints (e.g., [/v0/tts/stream/json](/reference/text-to-speech-tts/synthesize-json-streaming), [/v0/tts/stream/file](/reference/text-to-speech-tts/synthesize-file-streaming)).
- Ensure only a single generation is requested ([num_generations](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.num_generations) must be `1` or omitted).
- With `instant_mode` enabled, **requests incur a 10% higher cost** due to increased compute and resource requirements.
    
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

<details><summary><code>client.tts.<a href="src/hume/tts/client.py">synthesize_json_streaming</a>(...)</code></summary>
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
from hume.tts import FormatMp3, PostedContextWithUtterances, PostedUtterance

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.tts.synthesize_json_streaming(
    utterances=[
        PostedUtterance(
            text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
            description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
        )
    ],
    context=PostedContextWithUtterances(
        utterances=[
            PostedUtterance(
                text="How can people see beauty so differently?",
                description="A curious student with a clear and respectful tone, seeking clarification on Hume's ideas with a straightforward question.",
            )
        ],
    ),
    format=FormatMp3(),
)
for chunk in response:
    yield chunk

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

**utterances:** `typing.Sequence[PostedUtterance]` 

A list of **Utterances** to be converted to speech output.

An **Utterance** is a unit of input for [Octave](/docs/text-to-speech-tts/overview), and includes input `text`, an optional `description` to serve as the prompt for how the speech should be delivered, an optional `voice` specification, and additional controls to guide delivery for `speed` and `trailing_silence`.
    
</dd>
</dl>

<dl>
<dd>

**context:** `typing.Optional[PostedContext]` — Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    
</dd>
</dl>

<dl>
<dd>

**format:** `typing.Optional[Format]` — Specifies the output audio file format.
    
</dd>
</dl>

<dl>
<dd>

**num_generations:** `typing.Optional[int]` — Number of generations of the audio to produce.
    
</dd>
</dl>

<dl>
<dd>

**split_utterances:** `typing.Optional[bool]` 

Controls how audio output is segmented in the response.

- When **enabled** (`true`), input utterances are automatically split into natural-sounding speech segments.

- When **disabled** (`false`), the response maintains a strict one-to-one mapping between input utterances and output snippets. 

This setting affects how the `snippets` array is structured in the response, which may be important for applications that need to track the relationship between input text and generated audio segments. When setting to `false`, avoid including utterances with long `text`, as this can result in distorted output.
    
</dd>
</dl>

<dl>
<dd>

**strip_headers:** `typing.Optional[bool]` — If enabled, the audio for all the chunks of a generation, once concatenated together, will constitute a single audio file. Otherwise, if disabled, each chunk's audio will be its own audio file, each with its own headers (if applicable).
    
</dd>
</dl>

<dl>
<dd>

**instant_mode:** `typing.Optional[bool]` 

Enables ultra-low latency streaming, significantly reducing the time until the first audio chunk is received. Recommended for real-time applications requiring immediate audio playback. For further details, see our documentation on [instant mode](/docs/text-to-speech-tts/overview#ultra-low-latency-streaming-instant-mode). 
- Dynamic voice generation is not supported with this mode; a predefined [voice](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.utterances.voice) must be specified in your request.
- This mode is only supported for streaming endpoints (e.g., [/v0/tts/stream/json](/reference/text-to-speech-tts/synthesize-json-streaming), [/v0/tts/stream/file](/reference/text-to-speech-tts/synthesize-file-streaming)).
- Ensure only a single generation is requested ([num_generations](/reference/text-to-speech-tts/synthesize-json-streaming#request.body.num_generations) must be `1` or omitted).
- With `instant_mode` enabled, **requests incur a 10% higher cost** due to increased compute and resource requirements.
    
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
<details><summary><code>client.tts.voices.<a href="src/hume/tts/voices/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists voices you have saved in your account, or voices from the [Voice Library](https://platform.hume.ai/tts/voice-library).
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.tts.voices.list(
    provider="CUSTOM_VOICE",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

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

- **`HUME_AI`**: Lists preset, shared voices from Hume's [Voice Library](https://platform.hume.ai/tts/voice-library).
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.voices.<a href="src/hume/tts/voices/client.py">create</a>(...)</code></summary>
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.tts.voices.create(
    generation_id="795c949a-1510-4a80-9646-7d0863b023ab",
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

**name:** `str` — Name of the voice in the `Voice Library`.
    
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

client = HumeClient(
    api_key="YOUR_API_KEY",
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

## EmpathicVoice Tools
<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">list_tools</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Tools**.

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.empathic_voice.tools.list_tools(
    page_number=0,
    page_size=2,
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

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

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">create_tool</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a **Tool** that can be added to an [EVI configuration](/reference/empathic-voice-interface-evi/configs/create-config).

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.create_tool(
    name="get_current_weather",
    parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
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

**name:** `str` — Name applied to all versions of a particular Tool.
    
</dd>
</dl>

<dl>
<dd>

**parameters:** `str` 

Stringified JSON defining the parameters used by this version of the Tool.

These parameters define the inputs needed for the Tool’s execution, including the expected data type and description for each input field. Structured as a stringified JSON schema, this format ensures the Tool receives data in the expected format.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Tool version.
    
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">list_tool_versions</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a list of a **Tool's** versions.

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.empathic_voice.tools.list_tool_versions(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

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

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">create_tool_version</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a **Tool** by creating a new version of the **Tool**.

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.create_tool_version(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
    parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
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

These parameters define the inputs needed for the Tool’s execution, including the expected data type and description for each input field. Structured as a stringified JSON schema, this format ensures the Tool receives data in the expected format.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Tool version.
    
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

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.delete_tool(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
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

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">update_tool_name</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the name of a **Tool**.

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.update_tool_name(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
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

**name:** `str` — Name applied to all versions of a particular Tool.
    
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

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">get_tool_version</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a specified version of a **Tool**.

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.get_tool_version(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
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

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.delete_tool_version(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
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

<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">update_tool_description</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the description of a specified **Tool** version.

Refer to our [tool use](/docs/empathic-voice-interface-evi/features/tool-use#function-calling) guide for comprehensive instructions on defining and integrating tools into EVI.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.update_tool_description(
    id="00183a3f-79ba-413d-9f3b-609864268bea",
    version=1,
    version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
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

## EmpathicVoice Prompts
<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">list_prompts</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a paginated list of **Prompts**.

See our [prompting guide](/docs/empathic-voice-interface-evi/guides/phone-calling) for tips on crafting your system prompt.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.empathic_voice.prompts.list_prompts(
    page_number=0,
    page_size=2,
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

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

**restrict_to_most_recent:** `typing.Optional[bool]` — Only include the most recent version of each prompt in the list.
    
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

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">create_prompt</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a **Prompt** that can be added to an [EVI configuration](/reference/empathic-voice-interface-evi/configs/create-config).

See our [prompting guide](/docs/empathic-voice-interface-evi/guides/phone-calling) for tips on crafting your system prompt.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
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

Instructions used to shape EVI’s behavior, responses, and style.

You can use the Prompt to define a specific goal or role for EVI, specifying how it should act or what it should focus on during the conversation. For example, EVI can be instructed to act as a customer support representative, a fitness coach, or a travel advisor, each with its own set of behaviors and response styles.

For help writing a system prompt, see our [Prompting Guide](/docs/empathic-voice-interface-evi/guides/prompting).
    
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

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">list_prompt_versions</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a list of a **Prompt's** versions.

See our [prompting guide](/docs/empathic-voice-interface-evi/guides/phone-calling) for tips on crafting your system prompt.
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

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.list_prompt_versions(
    id="af699d45-2985-42cc-91b9-af9e5da3bac5",
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

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">create_prompt_version</a>(...)</code></summary>
