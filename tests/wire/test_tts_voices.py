from .conftest import get_client, verify_request_count


def test_tts_voices_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "tts.voices.list_.0"
    client = get_client(test_id)
    client.tts.voices.list(provider="CUSTOM_VOICE")
    verify_request_count(test_id, "GET", "/v0/tts/voices", {"provider": "CUSTOM_VOICE"}, 1)


def test_tts_voices_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "tts.voices.create.0"
    client = get_client(test_id)
    client.tts.voices.create(generation_id="795c949a-1510-4a80-9646-7d0863b023ab", name="David Hume")
    verify_request_count(test_id, "POST", "/v0/tts/voices", None, 1)


def test_tts_voices_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "tts.voices.delete.0"
    client = get_client(test_id)
    client.tts.voices.delete(name="David Hume")
    verify_request_count(test_id, "DELETE", "/v0/tts/voices", {"name": "David Hume"}, 1)
