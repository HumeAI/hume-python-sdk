import os
from typing import Dict

import pytest

EvalData = Dict[str, str]


@pytest.fixture(scope="module")
def eval_data() -> EvalData:
    base_url = "https://storage.googleapis.com/hume-test-data"
    return {
        "image-obama-face": f"{base_url}/image/obama.png",
        "burst-amusement-009": f"{base_url}/audio/burst-amusement-009.mp3",
        "prosody-horror-1051": f"{base_url}/audio/prosody-horror-1051.mp3",
        "text-happy-place": f"{base_url}/text/happy.txt",
        "mesh-faces": f"{base_url}/landmarks/facelandmark_3face_test.json",
    }


@pytest.fixture(scope="session")
def hume_api_key() -> str:
    api_key = os.getenv("HUME_DEV_API_KEY")
    if api_key is None:
        raise ValueError("Cannot construct HumeBatchClient, HUME_DEV_API_KEY variable not set.")
    return api_key
