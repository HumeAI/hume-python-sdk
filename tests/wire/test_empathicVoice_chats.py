from .conftest import get_client, verify_request_count


def test_empathicVoice_chats_list_chats() -> None:
    """Test list-chats endpoint with WireMock"""
    test_id = "empathic_voice.chats.list_chats.0"
    client = get_client(test_id)
    client.empathic_voice.chats.list_chats(page_number=0, page_size=1, ascending_order=True)
    verify_request_count(
        test_id, "GET", "/v0/evi/chats", {"page_number": "0", "page_size": "1", "ascending_order": "true"}, 1
    )


def test_empathicVoice_chats_list_chat_events() -> None:
    """Test list-chat-events endpoint with WireMock"""
    test_id = "empathic_voice.chats.list_chat_events.0"
    client = get_client(test_id)
    client.empathic_voice.chats.list_chat_events(
        id="470a49f6-1dec-4afe-8b61-035d3b2d63b0", page_number=0, page_size=3, ascending_order=True
    )
    verify_request_count(
        test_id,
        "GET",
        "/v0/evi/chats/470a49f6-1dec-4afe-8b61-035d3b2d63b0",
        {"page_number": "0", "page_size": "3", "ascending_order": "true"},
        1,
    )


def test_empathicVoice_chats_get_audio() -> None:
    """Test get-audio endpoint with WireMock"""
    test_id = "empathic_voice.chats.get_audio.0"
    client = get_client(test_id)
    client.empathic_voice.chats.get_audio(id="470a49f6-1dec-4afe-8b61-035d3b2d63b0")
    verify_request_count(test_id, "GET", "/v0/evi/chats/470a49f6-1dec-4afe-8b61-035d3b2d63b0/audio", None, 1)
