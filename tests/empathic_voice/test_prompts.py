# This file was auto-generated by Fern from our API Definition.

import typing

from hume.client import AsyncHumeClient, HumeClient

from ..utilities import validate_response


async def test_create_prompt(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "version_description",
        "name": "name",
        "created_on": 1000000,
        "modified_on": 1000000,
        "text": "text",
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "text": None,
    }
    response = client.empathic_voice.prompts.create_prompt(name="name", text="text")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.prompts.create_prompt(name="name", text="text")
    validate_response(async_response, expected_response, expected_types)


async def test_list_prompt_versions(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "page_number": 1,
        "page_size": 1,
        "total_pages": 1,
        "prompts_page": [
            {
                "id": "id",
                "version": 1,
                "version_type": "FIXED",
                "version_description": "version_description",
                "name": "name",
                "created_on": 1000000,
                "modified_on": 1000000,
                "text": "text",
            }
        ],
    }
    expected_types: typing.Any = {
        "page_number": "integer",
        "page_size": "integer",
        "total_pages": "integer",
        "prompts_page": (
            "list",
            {
                0: {
                    "id": None,
                    "version": "integer",
                    "version_type": None,
                    "version_description": None,
                    "name": None,
                    "created_on": None,
                    "modified_on": None,
                    "text": None,
                }
            },
        ),
    }
    response = client.empathic_voice.prompts.list_prompt_versions(id="id")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.prompts.list_prompt_versions(id="id")
    validate_response(async_response, expected_response, expected_types)


async def test_create_prompt_verison(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "version_description",
        "name": "name",
        "created_on": 1000000,
        "modified_on": 1000000,
        "text": "text",
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "text": None,
    }
    response = client.empathic_voice.prompts.create_prompt_verison(id="id", text="text")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.prompts.create_prompt_verison(id="id", text="text")
    validate_response(async_response, expected_response, expected_types)


async def test_delete_prompt(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert client.empathic_voice.prompts.delete_prompt(id="id") is None  # type: ignore[func-returns-value]

    assert await async_client.empathic_voice.prompts.delete_prompt(id="id") is None  # type: ignore[func-returns-value]


async def test_update_prompt_name(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = "string"
    expected_types: typing.Any = None
    response = client.empathic_voice.prompts.update_prompt_name(id="string", name="string")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.prompts.update_prompt_name(id="string", name="string")
    validate_response(async_response, expected_response, expected_types)


async def test_get_prompt_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "version_description",
        "name": "name",
        "created_on": 1000000,
        "modified_on": 1000000,
        "text": "text",
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "text": None,
    }
    response = client.empathic_voice.prompts.get_prompt_version(id="id", version=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.prompts.get_prompt_version(id="id", version=1)
    validate_response(async_response, expected_response, expected_types)


async def test_delete_prompt_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert client.empathic_voice.prompts.delete_prompt_version(id="id", version=1) is None  # type: ignore[func-returns-value]

    assert await async_client.empathic_voice.prompts.delete_prompt_version(id="id", version=1) is None  # type: ignore[func-returns-value]


async def test_update_prompt_description(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "version": 1,
        "version_type": "FIXED",
        "version_description": "version_description",
        "name": "name",
        "created_on": 1000000,
        "modified_on": 1000000,
        "text": "text",
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_type": None,
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "text": None,
    }
    response = client.empathic_voice.prompts.update_prompt_description(id="id", version=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.prompts.update_prompt_description(id="id", version=1)
    validate_response(async_response, expected_response, expected_types)
