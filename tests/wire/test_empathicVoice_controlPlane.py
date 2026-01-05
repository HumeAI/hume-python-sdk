from .conftest import get_client, verify_request_count


def test_empathicVoice_controlPlane_send() -> None:
    """Test send endpoint with WireMock"""
    test_id = "empathic_voice.control_plane.send.0"
    client = get_client(test_id)
    client.empathic_voice.control_plane.send(chat_id="chat_id", request={"type": "session_settings"})
    verify_request_count(test_id, "POST", "/v0/evi/chat/chat_id/send", None, 1)
