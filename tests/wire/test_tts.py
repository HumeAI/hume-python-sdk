from .conftest import get_client, verify_request_count


def test_tts_synthesize_json() -> None:
    """Test synthesize-json endpoint with WireMock"""
    test_id = "tts.synthesize_json.0"
    client = get_client(test_id)
    client.tts.synthesize_json(
        context={},
        format={"type": "mp3"},
        num_generations=1,
        utterances=[
            {
                "text": "Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                "description": "Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
            }
        ],
    )
    verify_request_count(test_id, "POST", "/v0/tts", None, 1)


def test_tts_synthesize_file() -> None:
    """Test synthesize-file endpoint with WireMock"""
    test_id = "tts.synthesize_file.0"
    client = get_client(test_id)
    client.tts.synthesize_file(
        context={"generation_id": "09ad914d-8e7f-40f8-a279-e34f07f7dab2"},
        format={"type": "mp3"},
        num_generations=1,
        utterances=[
            {
                "text": "Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                "description": "Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
            }
        ],
    )
    verify_request_count(test_id, "POST", "/v0/tts/file", None, 1)


def test_tts_synthesize_file_streaming() -> None:
    """Test synthesize-file-streaming endpoint with WireMock"""
    test_id = "tts.synthesize_file_streaming.0"
    client = get_client(test_id)
    client.tts.synthesize_file_streaming(
        utterances=[
            {
                "text": "Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                "voice": {"provider": "HUME_AI"},
            }
        ]
    )
    verify_request_count(test_id, "POST", "/v0/tts/stream/file", None, 1)


def test_tts_synthesize_json_streaming() -> None:
    """Test synthesize-json-streaming endpoint with WireMock"""
    test_id = "tts.synthesize_json_streaming.0"
    client = get_client(test_id)
    client.tts.synthesize_json_streaming(
        utterances=[
            {
                "text": "Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                "voice": {"provider": "HUME_AI"},
            }
        ]
    )
    verify_request_count(test_id, "POST", "/v0/tts/stream/json", None, 1)


def test_tts_convert_voice_json() -> None:
    """Test convertVoiceJson endpoint with WireMock"""
    test_id = "tts.convert_voice_json.0"
    client = get_client(test_id)
    client.tts.convert_voice_json(audio="example_audio")
    verify_request_count(test_id, "POST", "/v0/tts/voice_conversion/json", None, 1)
