# Reference
## ExpressionMeasurement Batch
<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">list_jobs</a>(...)</code></summary>
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
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
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

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">start_inference_job</a>(...)</code></summary>
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
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.expression_measurement.batch.start_inference_job(
    urls=["https://hume-tutorials.s3.amazonaws.com/faces.zip"],
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

**models:** `typing.Optional[Models]` 

Specify the models to use for inference.

If this field is not explicitly set, then all models will run by default.
    
</dd>
</dl>

<dl>
<dd>

**transcription:** `typing.Optional[Transcription]` 
    
</dd>
</dl>

<dl>
<dd>

**urls:** `typing.Optional[typing.Sequence[str]]` 

URLs to the media files to be processed. Each must be a valid public URL to a media file (see recommended input filetypes) or an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`) of media files.

If you wish to supply more than 100 URLs, consider providing them as an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`).
    
</dd>
</dl>

<dl>
<dd>

**registry_files:** `typing.Optional[typing.Sequence[str]]` — List of File IDs corresponding to the files in the asset registry.
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[typing.Sequence[str]]` — Text supplied directly to our Emotional Language and NER models for analysis.
    
</dd>
</dl>

<dl>
<dd>

**callback_url:** `typing.Optional[str]` — If provided, a `POST` request will be made to the URL with the generated predictions on completion or the error message on failure.
    
</dd>
</dl>

<dl>
<dd>

**notify:** `typing.Optional[bool]` — Whether to send an email notification to the user upon job completion/failure.
    
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

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">get_job_details</a>(...)</code></summary>
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
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
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

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">get_job_predictions</a>(...)</code></summary>
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
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
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

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">get_job_artifacts</a>(...)</code></summary>
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
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.expression_measurement.batch.get_job_artifacts(
    id="string",
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

<details><summary><code>client.expression_measurement.batch.<a href="src/hume/expression_measurement/batch/client.py">start_inference_job_from_local_file</a>(...)</code></summary>
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
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.expression_measurement.batch.start_inference_job_from_local_file()

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

**file:** `from __future__ import annotations

typing.List[core.File]` — See core.File for more documentation
    
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

## EmpathicVoice Tools
<details><summary><code>client.empathic_voice.tools.<a href="src/hume/empathic_voice/tools/client.py">list_tools</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

**name:** `typing.Optional[str]` — Filter to only include tools with this name.
    
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.tools.list_tool_versions(
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

Tools, as well as Configs and Prompts, are versioned. This versioning system supports iterative development, allowing you to progressively refine tools and revert to previous versions if needed.

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

Tools, as well as Configs and Prompts, are versioned. This versioning system supports iterative development, allowing you to progressively refine tools and revert to previous versions if needed.

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

Tools, as well as Configs and Prompts, are versioned. This versioning system supports iterative development, allowing you to progressively refine tools and revert to previous versions if needed.

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

**restrict_to_most_recent:** `typing.Optional[bool]` — By default, `restrict_to_most_recent` is set to true, returning only the latest version of each prompt. To include all versions of each prompt in the list, set `restrict_to_most_recent` to false.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Filter to only include prompts with this name.
    
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

For help writing a system prompt, see our [Prompting Guide](/docs/empathic-voice-interface-evi/prompting).
    
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

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

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">create_prompt_verison</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.create_prompt_verison(
    id="af699d45-2985-42cc-91b9-af9e5da3bac5",
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

Instructions used to shape EVI’s behavior, responses, and style for this version of the Prompt.

You can use the Prompt to define a specific goal or role for EVI, specifying how it should act or what it should focus on during the conversation. For example, EVI can be instructed to act as a customer support representative, a fitness coach, or a travel advisor, each with its own set of behaviors and response styles.

For help writing a system prompt, see our [Prompting Guide](/docs/empathic-voice-interface-evi/prompting).
    
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.delete_prompt(
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">update_prompt_name</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.update_prompt_name(
    id="af699d45-2985-42cc-91b9-af9e5da3bac5",
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

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">get_prompt_version</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.get_prompt_version(
    id="af699d45-2985-42cc-91b9-af9e5da3bac5",
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

Prompts, as well as Configs and Tools, are versioned. This versioning system supports iterative development, allowing you to progressively refine prompts and revert to previous versions if needed.

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.delete_prompt_version(
    id="af699d45-2985-42cc-91b9-af9e5da3bac5",
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

Prompts, as well as Configs and Tools, are versioned. This versioning system supports iterative development, allowing you to progressively refine prompts and revert to previous versions if needed.

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

<details><summary><code>client.empathic_voice.prompts.<a href="src/hume/empathic_voice/prompts/client.py">update_prompt_description</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.prompts.update_prompt_description(
    id="af699d45-2985-42cc-91b9-af9e5da3bac5",
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

Prompts, as well as Configs and Tools, are versioned. This versioning system supports iterative development, allowing you to progressively refine prompts and revert to previous versions if needed.

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

## EmpathicVoice Configs
<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">list_configs</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
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

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">create_config</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient
from hume.empathic_voice import (
    PostedEventMessageSpec,
    PostedEventMessageSpecs,
    PostedLanguageModel,
    PostedPromptSpec,
    PostedVoice,
)

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.create_config(
    name="Weather Assistant Config",
    prompt=PostedPromptSpec(
        id="af699d45-2985-42cc-91b9-af9e5da3bac5",
        version=0,
    ),
    voice=PostedVoice(
        name="KORA",
    ),
    language_model=PostedLanguageModel(
        model_provider="ANTHROPIC",
        model_resource="claude-3-5-sonnet-20240620",
        temperature=1.0,
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

**name:** `str` — Name applied to all versions of a particular Config.
    
</dd>
</dl>

<dl>
<dd>

**version_description:** `typing.Optional[str]` — An optional description of the Config version.
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[PostedPromptSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**voice:** `typing.Optional[PostedVoice]` — A voice specification associated with this Config.
    
</dd>
</dl>

<dl>
<dd>

**language_model:** `typing.Optional[PostedLanguageModel]` 

The supplemental language model associated with this Config.

This model is used to generate longer, more detailed responses from EVI. Choosing an appropriate supplemental language model for your use case is crucial for generating fast, high-quality responses from EVI.
    
</dd>
</dl>

<dl>
<dd>

**ellm_model:** `typing.Optional[PostedEllmModel]` 

The eLLM setup associated with this Config.

Hume's eLLM (empathic Large Language Model) is a multimodal language model that takes into account both expression measures and language. The eLLM generates short, empathic language responses and guides text-to-speech (TTS) prosody.
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.Sequence[typing.Optional[PostedUserDefinedToolSpec]]]` — List of user-defined tools associated with this Config.
    
</dd>
</dl>

<dl>
<dd>

**builtin_tools:** `typing.Optional[typing.Sequence[typing.Optional[PostedBuiltinTool]]]` — List of built-in tools associated with this Config.
    
</dd>
</dl>

<dl>
<dd>

**event_messages:** `typing.Optional[PostedEventMessageSpecs]` 
    
</dd>
</dl>

<dl>
<dd>

**timeouts:** `typing.Optional[PostedTimeoutSpecs]` 
    
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

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">list_config_versions</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.list_config_versions(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">create_config_version</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient
from hume.empathic_voice import (
    PostedEllmModel,
    PostedEventMessageSpec,
    PostedEventMessageSpecs,
    PostedLanguageModel,
    PostedPromptSpec,
    PostedVoice,
)

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.create_config_version(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
    version_description="This is an updated version of the Weather Assistant Config.",
    prompt=PostedPromptSpec(
        id="af699d45-2985-42cc-91b9-af9e5da3bac5",
        version=0,
    ),
    voice=PostedVoice(
        name="ITO",
    ),
    language_model=PostedLanguageModel(
        model_provider="ANTHROPIC",
        model_resource="claude-3-5-sonnet-20240620",
        temperature=1.0,
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

**version_description:** `typing.Optional[str]` — An optional description of the Config version.
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `typing.Optional[PostedPromptSpec]` 
    
</dd>
</dl>

<dl>
<dd>

**voice:** `typing.Optional[PostedVoice]` — A voice specification associated with this Config version.
    
</dd>
</dl>

<dl>
<dd>

**language_model:** `typing.Optional[PostedLanguageModel]` 

The supplemental language model associated with this Config version.

This model is used to generate longer, more detailed responses from EVI. Choosing an appropriate supplemental language model for your use case is crucial for generating fast, high-quality responses from EVI.
    
</dd>
</dl>

<dl>
<dd>

**ellm_model:** `typing.Optional[PostedEllmModel]` 

The eLLM setup associated with this Config version.

Hume's eLLM (empathic Large Language Model) is a multimodal language model that takes into account both expression measures and language. The eLLM generates short, empathic language responses and guides text-to-speech (TTS) prosody.
    
</dd>
</dl>

<dl>
<dd>

**tools:** `typing.Optional[typing.Sequence[typing.Optional[PostedUserDefinedToolSpec]]]` — List of user-defined tools associated with this Config version.
    
</dd>
</dl>

<dl>
<dd>

**builtin_tools:** `typing.Optional[typing.Sequence[typing.Optional[PostedBuiltinTool]]]` — List of built-in tools associated with this Config version.
    
</dd>
</dl>

<dl>
<dd>

**event_messages:** `typing.Optional[PostedEventMessageSpecs]` 
    
</dd>
</dl>

<dl>
<dd>

**timeouts:** `typing.Optional[PostedTimeoutSpecs]` 
    
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.delete_config(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">update_config_name</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.update_config_name(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">get_config_version</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.get_config_version(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

Configs, as well as Prompts and Tools, are versioned. This versioning system supports iterative development, allowing you to progressively refine configurations and revert to previous versions if needed.

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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.delete_config_version(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

Configs, as well as Prompts and Tools, are versioned. This versioning system supports iterative development, allowing you to progressively refine configurations and revert to previous versions if needed.

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

<details><summary><code>client.empathic_voice.configs.<a href="src/hume/empathic_voice/configs/client.py">update_config_description</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.configs.update_config_description(
    id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

Configs, as well as Prompts and Tools, are versioned. This versioning system supports iterative development, allowing you to progressively refine configurations and revert to previous versions if needed.

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

## EmpathicVoice Chats
<details><summary><code>client.empathic_voice.chats.<a href="src/hume/empathic_voice/chats/client.py">list_chats</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.empathic_voice.chats.list_chats(
    page_number=0,
    page_size=1,
    ascending_order=True,
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

<details><summary><code>client.empathic_voice.chats.<a href="src/hume/empathic_voice/chats/client.py">list_chat_events</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.empathic_voice.chats.list_chat_events(
    id="470a49f6-1dec-4afe-8b61-035d3b2d63b0",
    page_number=0,
    page_size=3,
    ascending_order=True,
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

## EmpathicVoice ChatGroups
<details><summary><code>client.empathic_voice.chat_groups.<a href="src/hume/empathic_voice/chat_groups/client.py">list_chat_groups</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.chat_groups.list_chat_groups(
    page_number=0,
    page_size=1,
    ascending_order=True,
    config_id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
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

<details><summary><code>client.empathic_voice.chat_groups.<a href="src/hume/empathic_voice/chat_groups/client.py">list_chat_group_events</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from hume.client import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.empathic_voice.chat_groups.list_chat_group_events(
    id="697056f0-6c7e-487d-9bd8-9c19df79f05f",
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

