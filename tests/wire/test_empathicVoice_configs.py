from .conftest import get_client, verify_request_count


def test_empathicVoice_configs_list_configs() -> None:
    """Test list-configs endpoint with WireMock"""
    test_id = "empathic_voice.configs.list_configs.0"
    client = get_client(test_id)
    client.empathic_voice.configs.list_configs(page_number=0, page_size=1)
    verify_request_count(test_id, "GET", "/v0/evi/configs", {"page_number": "0", "page_size": "1"}, 1)


def test_empathicVoice_configs_create_config() -> None:
    """Test create-config endpoint with WireMock"""
    test_id = "empathic_voice.configs.create_config.0"
    client = get_client(test_id)
    client.empathic_voice.configs.create_config(
        name="Weather Assistant Config",
        prompt={"id": "af699d45-2985-42cc-91b9-af9e5da3bac5", "version": 0},
        evi_version="3",
        voice={"provider": "HUME_AI"},
        language_model={"model_provider": "ANTHROPIC", "model_resource": "claude-3-7-sonnet-latest", "temperature": 1},
        event_messages={
            "on_new_chat": {"enabled": False, "text": ""},
            "on_inactivity_timeout": {"enabled": False, "text": ""},
            "on_max_duration_timeout": {"enabled": False, "text": ""},
        },
    )
    verify_request_count(test_id, "POST", "/v0/evi/configs", None, 1)


def test_empathicVoice_configs_list_config_versions() -> None:
    """Test list-config-versions endpoint with WireMock"""
    test_id = "empathic_voice.configs.list_config_versions.0"
    client = get_client(test_id)
    client.empathic_voice.configs.list_config_versions(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3")
    verify_request_count(test_id, "GET", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3", None, 1)


def test_empathicVoice_configs_create_config_version() -> None:
    """Test create-config-version endpoint with WireMock"""
    test_id = "empathic_voice.configs.create_config_version.0"
    client = get_client(test_id)
    client.empathic_voice.configs.create_config_version(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        version_description="This is an updated version of the Weather Assistant Config.",
        evi_version="3",
        prompt={"id": "af699d45-2985-42cc-91b9-af9e5da3bac5", "version": 0},
        voice={"provider": "HUME_AI"},
        language_model={"model_provider": "ANTHROPIC", "model_resource": "claude-3-7-sonnet-latest", "temperature": 1},
        ellm_model={"allow_short_responses": True},
        event_messages={
            "on_new_chat": {"enabled": False, "text": ""},
            "on_inactivity_timeout": {"enabled": False, "text": ""},
            "on_max_duration_timeout": {"enabled": False, "text": ""},
        },
    )
    verify_request_count(test_id, "POST", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3", None, 1)


def test_empathicVoice_configs_delete_config() -> None:
    """Test delete-config endpoint with WireMock"""
    test_id = "empathic_voice.configs.delete_config.0"
    client = get_client(test_id)
    client.empathic_voice.configs.delete_config(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3")
    verify_request_count(test_id, "DELETE", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3", None, 1)


def test_empathicVoice_configs_update_config_name() -> None:
    """Test update-config-name endpoint with WireMock"""
    test_id = "empathic_voice.configs.update_config_name.0"
    client = get_client(test_id)
    client.empathic_voice.configs.update_config_name(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", name="Updated Weather Assistant Config Name"
    )
    verify_request_count(test_id, "PATCH", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3", None, 1)


def test_empathicVoice_configs_get_config_version() -> None:
    """Test get-config-version endpoint with WireMock"""
    test_id = "empathic_voice.configs.get_config_version.0"
    client = get_client(test_id)
    client.empathic_voice.configs.get_config_version(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", version=1)
    verify_request_count(test_id, "GET", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3/version/1", None, 1)


def test_empathicVoice_configs_delete_config_version() -> None:
    """Test delete-config-version endpoint with WireMock"""
    test_id = "empathic_voice.configs.delete_config_version.0"
    client = get_client(test_id)
    client.empathic_voice.configs.delete_config_version(id="1b60e1a0-cc59-424a-8d2c-189d354db3f3", version=1)
    verify_request_count(test_id, "DELETE", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3/version/1", None, 1)


def test_empathicVoice_configs_update_config_description() -> None:
    """Test update-config-description endpoint with WireMock"""
    test_id = "empathic_voice.configs.update_config_description.0"
    client = get_client(test_id)
    client.empathic_voice.configs.update_config_description(
        id="1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        version=1,
        version_description="This is an updated version_description.",
    )
    verify_request_count(test_id, "PATCH", "/v0/evi/configs/1b60e1a0-cc59-424a-8d2c-189d354db3f3/version/1", None, 1)
