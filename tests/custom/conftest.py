import os

import pytest

from utilities.eval_data import EvalData


@pytest.fixture(scope="module")
def eval_data() -> EvalData:
    base_url = "https://storage.googleapis.com/hume-test-data"
    return {
        "image-obama-face": f"{base_url}/image/obama.png",
        "burst-amusement-009": f"{base_url}/audio/burst-amusement-009.mp3",
        "prosody-horror-1051": f"{base_url}/audio/prosody-horror-1051.mp3",
        "prosody-noticias": f"{base_url}/audio/prosody-noticias.mp3",
        "know-any-good-jokes": f"{base_url}/audio/know-any-good-jokes.mp3",
        "weather-in-la": f"{base_url}/audio/weather-in-la.wav",
        "text-happy-place": f"{base_url}/text/happy.txt",
        "text-obama-news": f"{base_url}/text/obama.txt",
        "three-faces-mediapipe": f"{base_url}/landmarks/three-faces-mediapipe.json",
    }


@pytest.fixture(scope="session")
def hume_api_key() -> str:
    api_key = os.getenv("HUME_DEV_API_KEY")
    if api_key is None:
        raise ValueError("HUME_DEV_API_KEY environment variable is required.")
    return api_key
