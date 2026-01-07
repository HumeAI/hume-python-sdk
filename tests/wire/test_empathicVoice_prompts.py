from .conftest import get_client, verify_request_count


def test_empathicVoice_prompts_list_prompts() -> None:
    """Test list-prompts endpoint with WireMock"""
    test_id = "empathic_voice.prompts.list_prompts.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.list_prompts(page_number=0, page_size=2)
    verify_request_count(test_id, "GET", "/v0/evi/prompts", {"page_number": "0", "page_size": "2"}, 1)


def test_empathicVoice_prompts_create_prompt() -> None:
    """Test create-prompt endpoint with WireMock"""
    test_id = "empathic_voice.prompts.create_prompt.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.create_prompt(
        name="Weather Assistant Prompt",
        text="<role>You are an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
    )
    verify_request_count(test_id, "POST", "/v0/evi/prompts", None, 1)


def test_empathicVoice_prompts_list_prompt_versions() -> None:
    """Test list-prompt-versions endpoint with WireMock"""
    test_id = "empathic_voice.prompts.list_prompt_versions.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.list_prompt_versions(id="af699d45-2985-42cc-91b9-af9e5da3bac5")
    verify_request_count(test_id, "GET", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5", None, 1)


def test_empathicVoice_prompts_create_prompt_version() -> None:
    """Test create-prompt-version endpoint with WireMock"""
    test_id = "empathic_voice.prompts.create_prompt_version.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.create_prompt_version(
        id="af699d45-2985-42cc-91b9-af9e5da3bac5",
        text="<role>You are an updated version of an AI weather assistant providing users with accurate and up-to-date weather information. Respond to user queries concisely and clearly. Use simple language and avoid technical jargon. Provide temperature, precipitation, wind conditions, and any weather alerts. Include helpful tips if severe weather is expected.</role>",
        version_description="This is an updated version of the Weather Assistant Prompt.",
    )
    verify_request_count(test_id, "POST", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5", None, 1)


def test_empathicVoice_prompts_delete_prompt() -> None:
    """Test delete-prompt endpoint with WireMock"""
    test_id = "empathic_voice.prompts.delete_prompt.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.delete_prompt(id="af699d45-2985-42cc-91b9-af9e5da3bac5")
    verify_request_count(test_id, "DELETE", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5", None, 1)


def test_empathicVoice_prompts_update_prompt_name() -> None:
    """Test update-prompt-name endpoint with WireMock"""
    test_id = "empathic_voice.prompts.update_prompt_name.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.update_prompt_name(
        id="af699d45-2985-42cc-91b9-af9e5da3bac5", name="Updated Weather Assistant Prompt Name"
    )
    verify_request_count(test_id, "PATCH", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5", None, 1)


def test_empathicVoice_prompts_get_prompt_version() -> None:
    """Test get-prompt-version endpoint with WireMock"""
    test_id = "empathic_voice.prompts.get_prompt_version.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.get_prompt_version(id="af699d45-2985-42cc-91b9-af9e5da3bac5", version=0)
    verify_request_count(test_id, "GET", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5/version/0", None, 1)


def test_empathicVoice_prompts_delete_prompt_version() -> None:
    """Test delete-prompt-version endpoint with WireMock"""
    test_id = "empathic_voice.prompts.delete_prompt_version.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.delete_prompt_version(id="af699d45-2985-42cc-91b9-af9e5da3bac5", version=1)
    verify_request_count(test_id, "DELETE", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5/version/1", None, 1)


def test_empathicVoice_prompts_update_prompt_description() -> None:
    """Test update-prompt-description endpoint with WireMock"""
    test_id = "empathic_voice.prompts.update_prompt_description.0"
    client = get_client(test_id)
    client.empathic_voice.prompts.update_prompt_description(
        id="af699d45-2985-42cc-91b9-af9e5da3bac5",
        version=1,
        version_description="This is an updated version_description.",
    )
    verify_request_count(test_id, "PATCH", "/v0/evi/prompts/af699d45-2985-42cc-91b9-af9e5da3bac5/version/1", None, 1)
