from .conftest import get_client, verify_request_count


def test_empathicVoice_tools_list_tools() -> None:
    """Test list-tools endpoint with WireMock"""
    test_id = "empathic_voice.tools.list_tools.0"
    client = get_client(test_id)
    client.empathic_voice.tools.list_tools(page_number=0, page_size=2)
    verify_request_count(test_id, "GET", "/v0/evi/tools", {"page_number": "0", "page_size": "2"}, 1)


def test_empathicVoice_tools_create_tool() -> None:
    """Test create-tool endpoint with WireMock"""
    test_id = "empathic_voice.tools.create_tool.0"
    client = get_client(test_id)
    client.empathic_voice.tools.create_tool(
        name="get_current_weather",
        parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
        version_description="Fetches current weather and uses celsius or fahrenheit based on location of user.",
        description="This tool is for getting the current weather.",
        fallback_content="Unable to fetch current weather.",
    )
    verify_request_count(test_id, "POST", "/v0/evi/tools", None, 1)


def test_empathicVoice_tools_list_tool_versions() -> None:
    """Test list-tool-versions endpoint with WireMock"""
    test_id = "empathic_voice.tools.list_tool_versions.0"
    client = get_client(test_id)
    client.empathic_voice.tools.list_tool_versions(id="00183a3f-79ba-413d-9f3b-609864268bea")
    verify_request_count(test_id, "GET", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea", None, 1)


def test_empathicVoice_tools_create_tool_version() -> None:
    """Test create-tool-version endpoint with WireMock"""
    test_id = "empathic_voice.tools.create_tool_version.0"
    client = get_client(test_id)
    client.empathic_voice.tools.create_tool_version(
        id="00183a3f-79ba-413d-9f3b-609864268bea",
        parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
        version_description="Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
        fallback_content="Unable to fetch current weather.",
        description="This tool is for getting the current weather.",
    )
    verify_request_count(test_id, "POST", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea", None, 1)


def test_empathicVoice_tools_delete_tool() -> None:
    """Test delete-tool endpoint with WireMock"""
    test_id = "empathic_voice.tools.delete_tool.0"
    client = get_client(test_id)
    client.empathic_voice.tools.delete_tool(id="00183a3f-79ba-413d-9f3b-609864268bea")
    verify_request_count(test_id, "DELETE", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea", None, 1)


def test_empathicVoice_tools_update_tool_name() -> None:
    """Test update-tool-name endpoint with WireMock"""
    test_id = "empathic_voice.tools.update_tool_name.0"
    client = get_client(test_id)
    client.empathic_voice.tools.update_tool_name(
        id="00183a3f-79ba-413d-9f3b-609864268bea", name="get_current_temperature"
    )
    verify_request_count(test_id, "PATCH", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea", None, 1)


def test_empathicVoice_tools_get_tool_version() -> None:
    """Test get-tool-version endpoint with WireMock"""
    test_id = "empathic_voice.tools.get_tool_version.0"
    client = get_client(test_id)
    client.empathic_voice.tools.get_tool_version(id="00183a3f-79ba-413d-9f3b-609864268bea", version=1)
    verify_request_count(test_id, "GET", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea/version/1", None, 1)


def test_empathicVoice_tools_delete_tool_version() -> None:
    """Test delete-tool-version endpoint with WireMock"""
    test_id = "empathic_voice.tools.delete_tool_version.0"
    client = get_client(test_id)
    client.empathic_voice.tools.delete_tool_version(id="00183a3f-79ba-413d-9f3b-609864268bea", version=1)
    verify_request_count(test_id, "DELETE", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea/version/1", None, 1)


def test_empathicVoice_tools_update_tool_description() -> None:
    """Test update-tool-description endpoint with WireMock"""
    test_id = "empathic_voice.tools.update_tool_description.0"
    client = get_client(test_id)
    client.empathic_voice.tools.update_tool_description(
        id="00183a3f-79ba-413d-9f3b-609864268bea",
        version=1,
        version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
    )
    verify_request_count(test_id, "PATCH", "/v0/evi/tools/00183a3f-79ba-413d-9f3b-609864268bea/version/1", None, 1)
