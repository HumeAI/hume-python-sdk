from .conftest import get_client, verify_request_count

from hume.tts import FormatMp3, PostedContextWithUtterances, PostedUtterance


def test_tts_synthesize_json() -> None:
    """Test synthesize-json endpoint with WireMock"""
    test_id = "tts.synthesize_json.0"
    client = get_client(test_id)
    client.tts.synthesize_json(
        context=PostedContextWithUtterances(
            utterances=[
                PostedUtterance(
                    text="How can people see beauty so differently?",
                    description="A curious student with a clear and respectful tone, seeking clarification on Hume's ideas with a straightforward question.",
                )
            ],
        ),
        format=FormatMp3(
            type="mp3",
        ),
        num_generations=1,
        utterances=[
            PostedUtterance(
                text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
            )
        ],
    )
    verify_request_count(test_id, "POST", "/v0/tts", None, 1)


def test_tts_synthesize_file() -> None:
    """Test synthesize-file endpoint with WireMock"""
    test_id = "tts.synthesize_file.0"
    client = get_client(test_id)
    for _ in client.tts.synthesize_file(
        context=PostedContextWithGenerationId(
            generation_id="",
        ),
        format=FormatMp3(
            type="mp3",
        ),
        num_generations=1,
        utterances=[
            PostedUtterance(
                text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                description="Middle-aged masculine voice with a clear, rhythmic Scots lilt, rounded vowels, and a warm, steady tone with an articulate, academic quality.",
            )
        ],
    ):
        pass
    verify_request_count(test_id, "POST", "/v0/tts/file", None, 1)


def test_tts_synthesize_file_streaming() -> None:
    """Test synthesize-file-streaming endpoint with WireMock"""
    test_id = "tts.synthesize_file_streaming.0"
    client = get_client(test_id)
    for _ in client.tts.synthesize_file_streaming(
        utterances=[
            PostedUtterance(
                text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                voice=PostedUtteranceVoiceWithName(
                    name="Male English Actor",
                    provider="HUME_AI",
                ),
            )
        ],
    ):
        pass
    verify_request_count(test_id, "POST", "/v0/tts/stream/file", None, 1)


def test_tts_synthesize_json_streaming() -> None:
    """Test synthesize-json-streaming endpoint with WireMock"""
    test_id = "tts.synthesize_json_streaming.0"
    client = get_client(test_id)
    for _ in client.tts.synthesize_json_streaming(
        utterances=[
            PostedUtterance(
                text="Beauty is no quality in things themselves: It exists merely in the mind which contemplates them.",
                voice=PostedUtteranceVoiceWithName(
                    name="Male English Actor",
                    provider="HUME_AI",
                ),
            )
        ],
    ):
        pass
    verify_request_count(test_id, "POST", "/v0/tts/stream/json", None, 1)


def test_tts_convert_voice_json() -> None:
    """Test convertVoiceJson endpoint with WireMock"""
    test_id = "tts.convert_voice_json.0"
    client = get_client(test_id)
    for _ in client.tts.convert_voice_json(
        audio="example_audio",
    ):
        pass
    verify_request_count(test_id, "POST", "/v0/tts/voice_conversion/json", None, 1)
