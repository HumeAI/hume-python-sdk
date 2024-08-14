# This file was auto-generated by Fern from our API Definition.

from hume import HumeClient
from hume import AsyncHumeClient
import typing
from ..utilities import validate_response
from hume.empathic_voice import PostedPromptSpec
from hume.empathic_voice import PostedVoice
from hume.empathic_voice import PostedLanguageModel
from hume.empathic_voice import PostedEventMessageSpecs
from hume.empathic_voice import PostedEventMessageSpec
from hume.empathic_voice import PostedEllmModel


async def test_list_configs(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "page_number": 0,
        "page_size": 1,
        "total_pages": 1,
        "configs_page": [
            {
                "id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
                "version": 0,
                "version_description": "",
                "name": "Weather Assistant Config",
                "created_on": 1715267200693,
                "modified_on": 1715267200693,
                "prompt": {
                    "id": "af699d45-2985-42cc-91b9-af9e5da3bac5",
                    "version": 0,
                    "version_type": "FIXED",
                    "version_description": "",
                    "name": "Weather Assistant Prompt",
                    "created_on": 1715267200693,
                    "modified_on": 1715267200693,
                    "text": "<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
                },
                "voice": {"provider": "HUME_AI", "name": "KORA"},
                "language_model": {
                    "model_provider": "ANTHROPIC",
                    "model_resource": "claude-3-5-sonnet-20240620",
                    "temperature": 1,
                },
                "ellm_model": {"allow_short_responses": False},
                "tools": [],
                "builtin_tools": [],
                "event_messages": {
                    "on_new_chat": {"enabled": False, "text": ""},
                    "on_inactivity_timeout": {"enabled": False, "text": ""},
                    "on_max_duration_timeout": {"enabled": False, "text": ""},
                },
                "timeouts": {
                    "inactivity": {"enabled": True, "duration_secs": 600},
                    "max_duration": {"enabled": True, "duration_secs": 1800},
                },
            }
        ],
    }
    expected_types: typing.Any = {
        "page_number": "integer",
        "page_size": "integer",
        "total_pages": "integer",
        "configs_page": (
            "list",
            {
                0: {
                    "id": None,
                    "version": "integer",
                    "version_description": None,
                    "name": None,
                    "created_on": None,
                    "modified_on": None,
                    "prompt": {
                        "id": None,
                        "version": "integer",
                        "version_type": None,
                        "version_description": None,
                        "name": None,
                        "created_on": None,
                        "modified_on": None,
                        "text": None,
                    },
                    "voice": {"provider": None, "name": None},
                    "language_model": {"model_provider": None, "model_resource": None, "temperature": None},
                    "ellm_model": {"allow_short_responses": None},
                    "tools": ("list", {}),
                    "builtin_tools": ("list", {}),
                    "event_messages": {
                        "on_new_chat": {"enabled": None, "text": None},
                        "on_inactivity_timeout": {"enabled": None, "text": None},
                        "on_max_duration_timeout": {"enabled": None, "text": None},
                    },
                    "timeouts": {
                        "inactivity": {"enabled": None, "duration_secs": "integer"},
                        "max_duration": {"enabled": None, "duration_secs": "integer"},
                    },
                }
            },
        ),
    }
    response = client.empathic_voice.configs.list_configs(page_number=0, page_size=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.configs.list_configs(page_number=0, page_size=1)
    validate_response(async_response, expected_response, expected_types)


async def test_create_config(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        "version": 0,
        "version_description": "",
        "name": "Weather Assistant Config",
        "created_on": 1715275452390,
        "modified_on": 1715275452390,
        "prompt": {
            "id": "af699d45-2985-42cc-91b9-af9e5da3bac5",
            "version": 0,
            "version_type": "FIXED",
            "version_description": "",
            "name": "Weather Assistant Prompt",
            "created_on": 1715267200693,
            "modified_on": 1715267200693,
            "text": "<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
        },
        "voice": {"provider": "HUME_AI", "name": "KORA"},
        "language_model": {
            "model_provider": "ANTHROPIC",
            "model_resource": "claude-3-5-sonnet-20240620",
            "temperature": 1,
        },
        "ellm_model": {"allow_short_responses": False},
        "tools": [],
        "builtin_tools": [],
        "event_messages": {
            "on_new_chat": {"enabled": False, "text": ""},
            "on_inactivity_timeout": {"enabled": False, "text": ""},
            "on_max_duration_timeout": {"enabled": False, "text": ""},
        },
        "timeouts": {
            "inactivity": {"enabled": True, "duration_secs": 600},
            "max_duration": {"enabled": True, "duration_secs": 1800},
        },
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "prompt": {
            "id": None,
            "version": "integer",
            "version_type": None,
            "version_description": None,
            "name": None,
            "created_on": None,
            "modified_on": None,
            "text": None,
        },
        "voice": {"provider": None, "name": None},
        "language_model": {"model_provider": None, "model_resource": None, "temperature": None},
        "ellm_model": {"allow_short_responses": None},
        "tools": ("list", {}),
        "builtin_tools": ("list", {}),
        "event_messages": {
            "on_new_chat": {"enabled": None, "text": None},
            "on_inactivity_timeout": {"enabled": None, "text": None},
            "on_max_duration_timeout": {"enabled": None, "text": None},
        },
        "timeouts": {
            "inactivity": {"enabled": None, "duration_secs": "integer"},
            "max_duration": {"enabled": None, "duration_secs": "integer"},
        },
    }
    response = client.empathic_voice.configs.create_config(
        name="Weather Assistant Config",
        prompt=PostedPromptSpec(id="af699d45-2985-42cc-91b9-af9e5da3bac5", version=0),
        voice=PostedVoice(name="KORA"),
        language_model=PostedLanguageModel(
            model_provider="ANTHROPIC", model_resource="claude-3-5-sonnet-20240620", temperature=1.0
        ),
        event_messages=PostedEventMessageSpecs(
            on_new_chat=PostedEventMessageSpec(enabled=False, text=""),
            on_inactivity_timeout=PostedEventMessageSpec(enabled=False, text=""),
            on_max_duration_timeout=PostedEventMessageSpec(enabled=False, text=""),
        ),
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.configs.create_config(
        name="Weather Assistant Config",
        prompt=PostedPromptSpec(id="af699d45-2985-42cc-91b9-af9e5da3bac5", version=0),
        voice=PostedVoice(name="KORA"),
        language_model=PostedLanguageModel(
            model_provider="ANTHROPIC", model_resource="claude-3-5-sonnet-20240620", temperature=1.0
        ),
        event_messages=PostedEventMessageSpecs(
            on_new_chat=PostedEventMessageSpec(enabled=False, text=""),
            on_inactivity_timeout=PostedEventMessageSpec(enabled=False, text=""),
            on_max_duration_timeout=PostedEventMessageSpec(enabled=False, text=""),
        ),
    )
    validate_response(async_response, expected_response, expected_types)


async def test_list_config_versions(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "page_number": 0,
        "page_size": 10,
        "total_pages": 1,
        "configs_page": [
            {
                "id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
                "version": 0,
                "version_description": "",
                "name": "Weather Assistant Config",
                "created_on": 1715275452390,
                "modified_on": 1715275452390,
                "prompt": {
                    "id": "af699d45-2985-42cc-91b9-af9e5da3bac5",
                    "version": 0,
                    "version_type": "FIXED",
                    "version_description": "",
                    "name": "Weather Assistant Prompt",
                    "created_on": 1715267200693,
                    "modified_on": 1715267200693,
                    "text": "<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
                },
                "voice": {"provider": "HUME_AI", "name": "KORA"},
                "language_model": {
                    "model_provider": "ANTHROPIC",
                    "model_resource": "claude-3-5-sonnet-20240620",
                    "temperature": 1,
                },
                "ellm_model": {"allow_short_responses": False},
                "tools": [],
                "builtin_tools": [],
                "event_messages": {
                    "on_new_chat": {"enabled": False, "text": ""},
                    "on_inactivity_timeout": {"enabled": False, "text": ""},
                    "on_max_duration_timeout": {"enabled": False, "text": ""},
                },
                "timeouts": {
                    "inactivity": {"enabled": True, "duration_secs": 600},
                    "max_duration": {"enabled": True, "duration_secs": 1800},
                },
            }
        ],
    }
    expected_types: typing.Any = {
        "page_number": "integer",
        "page_size": "integer",
        "total_pages": "integer",
        "configs_page": (
            "list",
            {
                0: {
                    "id": None,
                    "version": "integer",
                    "version_description": None,
                    "name": None,
                    "created_on": None,
                    "modified_on": None,
                    "prompt": {
                        "id": None,
                        "version": "integer",
                        "version_type": None,
                        "version_description": None,
                        "name": None,
                        "created_on": None,
                        "modified_on": None,
                        "text": None,
                    },
                    "voice": {"provider": None, "name": None},
                    "language_model": {"model_provider": None, "model_resource": None, "temperature": None},
                    "ellm_model": {"allow_short_responses": None},
                    "tools": ("list", {}),
                    "builtin_tools": ("list", {}),
                    "event_messages": {
                        "on_new_chat": {"enabled": None, "text": None},
                        "on_inactivity_timeout": {"enabled": None, "text": None},
                        "on_max_duration_timeout": {"enabled": None, "text": None},
                    },
                    "timeouts": {
                        "inactivity": {"enabled": None, "duration_secs": "integer"},
                        "max_duration": {"enabled": None, "duration_secs": "integer"},
                    },
                }
            },
        ),
    }
    response = client.empathic_voice.configs.list_config_versions(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.configs.list_config_versions(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3"
    )
    validate_response(async_response, expected_response, expected_types)


async def test_create_config_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        "version": 1,
        "version_description": "This is an updated version of the Weather Assistant Config.",
        "name": "Weather Assistant Config",
        "created_on": 1715275452390,
        "modified_on": 1722642242998,
        "prompt": {
            "id": "af699d45-2985-42cc-91b9-af9e5da3bac5",
            "version": 0,
            "version_type": "FIXED",
            "version_description": "",
            "name": "Weather Assistant Prompt",
            "created_on": 1715267200693,
            "modified_on": 1715267200693,
            "text": "<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
        },
        "voice": {"provider": "HUME_AI", "name": "ITO"},
        "language_model": {
            "model_provider": "ANTHROPIC",
            "model_resource": "claude-3-5-sonnet-20240620",
            "temperature": 1,
        },
        "ellm_model": {"allow_short_responses": True},
        "tools": [],
        "builtin_tools": [],
        "event_messages": {
            "on_new_chat": {"enabled": False, "text": ""},
            "on_inactivity_timeout": {"enabled": False, "text": ""},
            "on_max_duration_timeout": {"enabled": False, "text": ""},
        },
        "timeouts": {
            "inactivity": {"enabled": True, "duration_secs": 600},
            "max_duration": {"enabled": True, "duration_secs": 1800},
        },
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "prompt": {
            "id": None,
            "version": "integer",
            "version_type": None,
            "version_description": None,
            "name": None,
            "created_on": None,
            "modified_on": None,
            "text": None,
        },
        "voice": {"provider": None, "name": None},
        "language_model": {"model_provider": None, "model_resource": None, "temperature": None},
        "ellm_model": {"allow_short_responses": None},
        "tools": ("list", {}),
        "builtin_tools": ("list", {}),
        "event_messages": {
            "on_new_chat": {"enabled": None, "text": None},
            "on_inactivity_timeout": {"enabled": None, "text": None},
            "on_max_duration_timeout": {"enabled": None, "text": None},
        },
        "timeouts": {
            "inactivity": {"enabled": None, "duration_secs": "integer"},
            "max_duration": {"enabled": None, "duration_secs": "integer"},
        },
    }
    response = client.empathic_voice.configs.create_config_version(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        version_description="This is an updated version of the Weather Assistant Config.",
        prompt=PostedPromptSpec(id="af699d45-2985-42cc-91b9-af9e5da3bac5", version=0),
        voice=PostedVoice(name="ITO"),
        language_model=PostedLanguageModel(
            model_provider="ANTHROPIC", model_resource="claude-3-5-sonnet-20240620", temperature=1.0
        ),
        ellm_model=PostedEllmModel(allow_short_responses=True),
        event_messages=PostedEventMessageSpecs(
            on_new_chat=PostedEventMessageSpec(enabled=False, text=""),
            on_inactivity_timeout=PostedEventMessageSpec(enabled=False, text=""),
            on_max_duration_timeout=PostedEventMessageSpec(enabled=False, text=""),
        ),
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.configs.create_config_version(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        version_description="This is an updated version of the Weather Assistant Config.",
        prompt=PostedPromptSpec(id="af699d45-2985-42cc-91b9-af9e5da3bac5", version=0),
        voice=PostedVoice(name="ITO"),
        language_model=PostedLanguageModel(
            model_provider="ANTHROPIC", model_resource="claude-3-5-sonnet-20240620", temperature=1.0
        ),
        ellm_model=PostedEllmModel(allow_short_responses=True),
        event_messages=PostedEventMessageSpecs(
            on_new_chat=PostedEventMessageSpec(enabled=False, text=""),
            on_inactivity_timeout=PostedEventMessageSpec(enabled=False, text=""),
            on_max_duration_timeout=PostedEventMessageSpec(enabled=False, text=""),
        ),
    )
    validate_response(async_response, expected_response, expected_types)


async def test_delete_config(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.empathic_voice.configs.delete_config(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3")  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.empathic_voice.configs.delete_config(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3")  # type: ignore[func-returns-value]
        is None
    )


async def test_update_config_name(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.empathic_voice.configs.update_config_name(
            id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", name="Updated Weather Assistant Config Name"
        )  # type: ignore[func-returns-value]
        == ""
    )

    assert (
        await async_client.empathic_voice.configs.update_config_name(
            id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", name="Updated Weather Assistant Config Name"
        )  # type: ignore[func-returns-value]
        is None
    )


async def test_get_config_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        "version": 1,
        "version_description": "",
        "name": "Weather Assistant Config",
        "created_on": 1715275452390,
        "modified_on": 1715275452390,
        "prompt": {
            "id": "af699d45-2985-42cc-91b9-af9e5da3bac5",
            "version": 0,
            "version_type": "FIXED",
            "version_description": "",
            "name": "Weather Assistant Prompt",
            "created_on": 1715267200693,
            "modified_on": 1715267200693,
            "text": "<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
        },
        "voice": {"provider": "HUME_AI", "name": "KORA"},
        "language_model": {
            "model_provider": "ANTHROPIC",
            "model_resource": "claude-3-5-sonnet-20240620",
            "temperature": 1,
        },
        "ellm_model": {"allow_short_responses": False},
        "tools": [],
        "builtin_tools": [],
        "event_messages": {
            "on_new_chat": {"enabled": False, "text": ""},
            "on_inactivity_timeout": {"enabled": False, "text": ""},
            "on_max_duration_timeout": {"enabled": False, "text": ""},
        },
        "timeouts": {
            "inactivity": {"enabled": True, "duration_secs": 600},
            "max_duration": {"enabled": True, "duration_secs": 1800},
        },
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "prompt": {
            "id": None,
            "version": "integer",
            "version_type": None,
            "version_description": None,
            "name": None,
            "created_on": None,
            "modified_on": None,
            "text": None,
        },
        "voice": {"provider": None, "name": None},
        "language_model": {"model_provider": None, "model_resource": None, "temperature": None},
        "ellm_model": {"allow_short_responses": None},
        "tools": ("list", {}),
        "builtin_tools": ("list", {}),
        "event_messages": {
            "on_new_chat": {"enabled": None, "text": None},
            "on_inactivity_timeout": {"enabled": None, "text": None},
            "on_max_duration_timeout": {"enabled": None, "text": None},
        },
        "timeouts": {
            "inactivity": {"enabled": None, "duration_secs": "integer"},
            "max_duration": {"enabled": None, "duration_secs": "integer"},
        },
    }
    response = client.empathic_voice.configs.get_config_version(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", version=1)
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.configs.get_config_version(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", version=1
    )
    validate_response(async_response, expected_response, expected_types)


async def test_delete_config_version(client: HumeClient, async_client: AsyncHumeClient) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.empathic_voice.configs.delete_config_version(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", version=1)  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.empathic_voice.configs.delete_config_version(
            id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", version=1
        )  # type: ignore[func-returns-value]
        is None
    )


async def test_update_config_description(client: HumeClient, async_client: AsyncHumeClient) -> None:
    expected_response: typing.Any = {
        "id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        "version": 1,
        "version_description": "This is an updated version_description.",
        "name": "Weather Assistant Config",
        "created_on": 1715275452390,
        "modified_on": 1715275452390,
        "prompt": {
            "id": "af699d45-2985-42cc-91b9-af9e5da3bac5",
            "version": 0,
            "version_type": "FIXED",
            "version_description": "",
            "name": "Weather Assistant Prompt",
            "created_on": 1715267200693,
            "modified_on": 1715267200693,
            "text": "<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
        },
        "voice": {"provider": "HUME_AI", "name": "KORA"},
        "language_model": {
            "model_provider": "ANTHROPIC",
            "model_resource": "claude-3-5-sonnet-20240620",
            "temperature": 1,
        },
        "ellm_model": {"allow_short_responses": False},
        "tools": [],
        "builtin_tools": [],
        "event_messages": {
            "on_new_chat": {"enabled": False, "text": ""},
            "on_inactivity_timeout": {"enabled": False, "text": ""},
            "on_max_duration_timeout": {"enabled": False, "text": ""},
        },
        "timeouts": {
            "inactivity": {"enabled": True, "duration_secs": 600},
            "max_duration": {"enabled": True, "duration_secs": 1800},
        },
    }
    expected_types: typing.Any = {
        "id": None,
        "version": "integer",
        "version_description": None,
        "name": None,
        "created_on": None,
        "modified_on": None,
        "prompt": {
            "id": None,
            "version": "integer",
            "version_type": None,
            "version_description": None,
            "name": None,
            "created_on": None,
            "modified_on": None,
            "text": None,
        },
        "voice": {"provider": None, "name": None},
        "language_model": {"model_provider": None, "model_resource": None, "temperature": None},
        "ellm_model": {"allow_short_responses": None},
        "tools": ("list", {}),
        "builtin_tools": ("list", {}),
        "event_messages": {
            "on_new_chat": {"enabled": None, "text": None},
            "on_inactivity_timeout": {"enabled": None, "text": None},
            "on_max_duration_timeout": {"enabled": None, "text": None},
        },
        "timeouts": {
            "inactivity": {"enabled": None, "duration_secs": "integer"},
            "max_duration": {"enabled": None, "duration_secs": "integer"},
        },
    }
    response = client.empathic_voice.configs.update_config_description(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        version=1,
        version_description="This is an updated version_description.",
    )
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.empathic_voice.configs.update_config_description(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        version=1,
        version_description="This is an updated version_description.",
    )
    validate_response(async_response, expected_response, expected_types)
