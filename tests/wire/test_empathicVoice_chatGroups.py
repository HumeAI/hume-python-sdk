from .conftest import get_client, verify_request_count


def test_empathicVoice_chatGroups_list_chat_groups() -> None:
    """Test list-chat-groups endpoint with WireMock"""
    test_id = "empathic_voice.chat_groups.list_chat_groups.0"
    client = get_client(test_id)
    client.empathic_voice.chat_groups.list_chat_groups(
        page_number=0, page_size=1, ascending_order=True, config_id="1b60e1a0-cc59-424a-8d2c-189d354db3f3"
    )
    verify_request_count(
        test_id,
        "GET",
        "/v0/evi/chat_groups",
        {
            "page_number": "0",
            "page_size": "1",
            "ascending_order": "true",
            "config_id": "1b60e1a0-cc59-424a-8d2c-189d354db3f3",
        },
        1,
    )


def test_empathicVoice_chatGroups_get_chat_group() -> None:
    """Test get-chat-group endpoint with WireMock"""
    test_id = "empathic_voice.chat_groups.get_chat_group.0"
    client = get_client(test_id)
    client.empathic_voice.chat_groups.get_chat_group(
        id="697056f0-6c7e-487d-9bd8-9c19df79f05f", page_number=0, page_size=1, ascending_order=True
    )
    verify_request_count(
        test_id,
        "GET",
        "/v0/evi/chat_groups/697056f0-6c7e-487d-9bd8-9c19df79f05f",
        {"page_number": "0", "page_size": "1", "ascending_order": "true"},
        1,
    )


def test_empathicVoice_chatGroups_get_audio() -> None:
    """Test get-audio endpoint with WireMock"""
    test_id = "empathic_voice.chat_groups.get_audio.0"
    client = get_client(test_id)
    client.empathic_voice.chat_groups.get_audio(
        id="369846cf-6ad5-404d-905e-a8acb5cdfc78", page_number=0, page_size=10, ascending_order=True
    )
    verify_request_count(
        test_id,
        "GET",
        "/v0/evi/chat_groups/369846cf-6ad5-404d-905e-a8acb5cdfc78/audio",
        {"page_number": "0", "page_size": "10", "ascending_order": "true"},
        1,
    )


def test_empathicVoice_chatGroups_list_chat_group_events() -> None:
    """Test list-chat-group-events endpoint with WireMock"""
    test_id = "empathic_voice.chat_groups.list_chat_group_events.0"
    client = get_client(test_id)
    client.empathic_voice.chat_groups.list_chat_group_events(
        id="697056f0-6c7e-487d-9bd8-9c19df79f05f", page_number=0, page_size=3, ascending_order=True
    )
    verify_request_count(
        test_id,
        "GET",
        "/v0/evi/chat_groups/697056f0-6c7e-487d-9bd8-9c19df79f05f/events",
        {"page_number": "0", "page_size": "3", "ascending_order": "true"},
        1,
    )
