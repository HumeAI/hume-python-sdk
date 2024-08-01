# This file was auto-generated by Fern from our API Definition.

import typing

from hume.client import AsyncHumeClient, HumeClient

from ..utilities import validate_response


async def test_list_chat_groups(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "page_number": 1,
        "page_size": 1,
        "total_pages": 1,
        "pagination_direction": "ASC",
        "chat_groups_page": [
            {
                "id": "id",
                "first_start_timestamp": 1000000,
                "most_recent_start_timestamp": 1000000,
                "most_recent_chat_id": "most_recent_chat_id",
                "num_chats": 1,
                "active": True,
            }
        ],
    }
    expected_types: typing.Any = {
        "page_number": "integer",
        "page_size": "integer",
        "total_pages": "integer",
        "pagination_direction": None,
        "chat_groups_page": (
            "list",
            {
                0: {
                    "id": None,
                    "first_start_timestamp": None,
                    "most_recent_start_timestamp": None,
                    "most_recent_chat_id": None,
                    "num_chats": "integer",
                    "active": None,
                }
            },
        ),
    }
    response = client.empathic_voice.chat_groups.list_chat_groups()
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.chat_groups.list_chat_groups()
    validate_response(async_response, expected_response, expected_types)


async def test_list_chat_group_events(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "id",
        "page_number": 1,
        "page_size": 1,
        "total_pages": 1,
        "pagination_direction": "ASC",
        "events_page": [
            {
                "id": "id",
                "chat_id": "chat_id",
                "timestamp": 1000000,
                "role": "USER",
                "type": "SYSTEM_PROMPT",
                "message_text": "message_text",
                "emotion_features": "emotion_features",
                "metadata": "metadata",
            }
        ],
    }
    expected_types: typing.Any = {
        "id": None,
        "page_number": "integer",
        "page_size": "integer",
        "total_pages": "integer",
        "pagination_direction": None,
        "events_page": (
            "list",
            {
                0: {
                    "id": None,
                    "chat_id": None,
                    "timestamp": None,
                    "role": None,
                    "type": None,
                    "message_text": None,
                    "emotion_features": None,
                    "metadata": None,
                }
            },
        ),
    }
    response = client.empathic_voice.chat_groups.list_chat_group_events(id="id")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.chat_groups.list_chat_group_events(id="id")
    validate_response(async_response, expected_response, expected_types)
