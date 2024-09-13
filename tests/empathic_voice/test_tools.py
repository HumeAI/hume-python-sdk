# This file was auto-generated by Fern from our API Definition.

from hume import HumeClient
from hume import AsyncHumeClient
import typing
from ..utilities import validate_response


async def test_create_tool(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "tool_type": "FUNCTION",
        "id": "aa9b71c4-723c-47ff-9f83-1a1829e74376",
        "version": 0,
        "version_type": "FIXED",
        "version_description": "Fetches current weather and uses celsius or fahrenheit based on location of user.",
        "name": "get_current_weather",
        "created_on": 1715275452390,
        "modified_on": 1715275452390,
        "fallback_content": "Unable to fetch current weather.",
        "description": "This tool is for getting the current weather.",
        "parameters": '{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
    }
    expected_types: typing.Any = {
        "tool_type": None,
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "fallback_content": None,
        "description": None,
        "parameters": None,
    }
    response = client.empathic_voice.tools.create_tool(
        name="get_current_weather",
        parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
        version_description="Fetches current weather and uses celsius or fahrenheit based on location of user.",
        description="This tool is for getting the current weather.",
        fallback_content="Unable to fetch current weather.",
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.tools.create_tool(
        name="get_current_weather",
        parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
        version_description="Fetches current weather and uses celsius or fahrenheit based on location of user.",
        description="This tool is for getting the current weather.",
        fallback_content="Unable to fetch current weather.",
    )
    validate_response(async_response, expected_response, expected_types)


async def test_list_tool_versions(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "page_number": 0,
        "page_size": 10,
        "total_pages": 1,
        "tools_page": [
            {
                "tool_type": "FUNCTION",
                "id": "00183a3f-79ba-413d-9f3b-609864268bea",
                "version": 1,
                "version_type": "FIXED",
                "version_description": "Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
                "name": "get_current_weather",
                "created_on": 1715277014228,
                "modified_on": 1715277602313,
                "fallback_content": "Unable to fetch current weather.",
                "description": "This tool is for getting the current weather.",
                "parameters": '{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
            }
        ],
    }
    expected_types: typing.Any = {
        "page_number": "integer",
        "page_size": "integer",
        "total_pages": "integer",
        "tools_page": (
            "list",
            {
                0: {
                    "tool_type": None,
                    "id": None,
                    "version": "integer",
                    "version_type": None,
                    "version_description": None,
                    "name": None,
                    "created_on": None,
                    "modified_on": None,
                    "fallback_content": None,
                    "description": None,
                    "parameters": None,
                }
            },
        ),
    }
    response = client.empathic_voice.tools.list_tool_versions(id="00183a3f-79ba-413d-9f3b-609864268bea")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.tools.list_tool_versions(
        id="00183a3f-79ba-413d-9f3b-609864268bea"
    )
    validate_response(async_response, expected_response, expected_types)


async def test_create_tool_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "tool_type": "FUNCTION",
        "id": "00183a3f-79ba-413d-9f3b-609864268bea",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
        "name": "get_current_weather",
        "created_on": 1715277014228,
        "modified_on": 1715277602313,
        "fallback_content": "Unable to fetch current weather.",
        "description": "This tool is for getting the current weather.",
        "parameters": '{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
    }
    expected_types: typing.Any = {
        "tool_type": None,
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "fallback_content": None,
        "description": None,
        "parameters": None,
    }
    response = client.empathic_voice.tools.create_tool_version(
        id="00183a3f-79ba-413d-9f3b-609864268bea",
        parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
        version_description="Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
        fallback_content="Unable to fetch current weather.",
        description="This tool is for getting the current weather.",
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.tools.create_tool_version(
        id="00183a3f-79ba-413d-9f3b-609864268bea",
        parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
        version_description="Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
        fallback_content="Unable to fetch current weather.",
        description="This tool is for getting the current weather.",
    )
    validate_response(async_response, expected_response, expected_types)


async def test_delete_tool(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.empathic_voice.tools.delete_tool(id="00183a3f-79ba-413d-9f3b-609864268bea")  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.empathic_voice.tools.delete_tool(id="00183a3f-79ba-413d-9f3b-609864268bea")  # type: ignore[func-returns-value]
        is None
    )


async def test_update_tool_name(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.empathic_voice.tools.update_tool_name(
            id="00183a3f-79ba-413d-9f3b-609864268bea", name="get_current_temperature"
        )  # type: ignore[func-returns-value]
        == ""
    )

    assert (
        await async_client.empathic_voice.tools.update_tool_name(
            id="00183a3f-79ba-413d-9f3b-609864268bea", name="get_current_temperature"
        )  # type: ignore[func-returns-value]
        == ""
    )


async def test_get_tool_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "tool_type": "FUNCTION",
        "id": "00183a3f-79ba-413d-9f3b-609864268bea",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
        "name": "string",
        "created_on": 1715277014228,
        "modified_on": 1715277602313,
        "fallback_content": "Unable to fetch current weather.",
        "description": "This tool is for getting the current weather.",
        "parameters": '{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
    }
    expected_types: typing.Any = {
        "tool_type": None,
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "fallback_content": None,
        "description": None,
        "parameters": None,
    }
    response = client.empathic_voice.tools.get_tool_version(id="00183a3f-79ba-413d-9f3b-609864268bea", version=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.tools.get_tool_version(
        id="00183a3f-79ba-413d-9f3b-609864268bea", version=1
    )
    validate_response(async_response, expected_response, expected_types)


async def test_delete_tool_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.empathic_voice.tools.delete_tool_version(id="00183a3f-79ba-413d-9f3b-609864268bea", version=1)  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.empathic_voice.tools.delete_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea", version=1
        )  # type: ignore[func-returns-value]
        is None
    )


async def test_update_tool_description(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "tool_type": "FUNCTION",
        "id": "00183a3f-79ba-413d-9f3b-609864268bea",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
        "name": "string",
        "created_on": 1715277014228,
        "modified_on": 1715277602313,
        "fallback_content": "Unable to fetch current weather.",
        "description": "This tool is for getting the current weather.",
        "parameters": '{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
    }
    expected_types: typing.Any = {
        "tool_type": None,
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "fallback_content": None,
        "description": None,
        "parameters": None,
    }
    response = client.empathic_voice.tools.update_tool_description(
        id="00183a3f-79ba-413d-9f3b-609864268bea",
        version=1,
        version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.tools.update_tool_description(
        id="00183a3f-79ba-413d-9f3b-609864268bea",
        version=1,
        version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
    )
    validate_response(async_response, expected_response, expected_types)
